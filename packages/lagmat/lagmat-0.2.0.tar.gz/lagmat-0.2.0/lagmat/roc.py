
from .lagmat_func import lagmat
from .chopnan import chopnan
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


def val_to_roc(val):
    """Convert values (e.g. prices) to rate of change, or quotients

    Parameters:
    -----------
    x : ndarray (2D)
        Time series with the oldest observation in the first row
        and the latest observation in the last row.
        Values need to be ratio-scale, i.e. x>0

    Returns:
    --------
    roc : ndarray (2D)
        rate of change, or quotients.
        The first row will be nan, i.e. r[0,;]=np.nan

    Alternative:
    ------------
        def val_to_roc(val):
            y = np.empty(shape=x.shape)
            y[0, :] = np.nan
            y[1:, :] = x[1:, :] / x[:-1, :]
            return y
    """
    return val / lagmat(val, lags=[1])


def roc_to_val(roc, initial=1):
    """Convert rate of change, or quotients into values or prices

    Returns:
    --------
    roc : ndarray (2D)
        rate of change, or quotients.

    initial: int or list/tupel/array
        Start values to compound the growth rates from

    Returns:
    --------
    x : ndarray (2D)
        Time series with the oldest observation in the first row
        and the latest observation in the last row.
    """
    z = roc.copy()
    z[0, :] = initial
    return np.cumprod(z, axis=0)


class RoC(BaseEstimator, TransformerMixin):
    def __init__(self, initial=None, trimnan=True):
        self.initial = initial
        self.trimnan = trimnan

    def fit(self, X, y=None):
        # store the starting values
        if self.initial is None:
            if len(X.shape) is 1:
                self.initial = X[0]
            else:
                self.initial = X[0, :]
        # done
        return self

    def transform(self, X, copy=None):
        if self.trimnan:
            return chopnan(val_to_roc(X), nchop=1)
        else:
            return val_to_roc(X)

    def inverse_transform(self, Z, initial=None, copy=None):
        # Use the requested initial value, or use the fitted initial values
        if initial is None:
            initial = self.initial
        # Multiply initial values repeatly with the rate of change
        if self.trimnan:
            return roc_to_val(
                np.r_[np.zeros(shape=(1, Z.shape[1])), Z],
                initial=initial)
        else:
            return roc_to_val(Z, initial=initial)
