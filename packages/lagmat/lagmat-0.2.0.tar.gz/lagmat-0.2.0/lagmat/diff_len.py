from .lagmat_func import lagmat
import numpy as np


def diff_len(x, lengths=None):
    """Differences for different Subperiod Lengths

    Parameters:
    -----------
    x : ndarray (2D)
        Time series with the oldest observation in the first row
        and the latest observation in the last row.

    lengths : list of int
        List/tuple with different subperiod lengths.

    Returns:
    --------
    y : ndarray (2D)
        Differences y_t = x_t - x_{t - m}
    """
    return np.tile(x, len(lengths)) - lagmat(x, lags=lengths)
