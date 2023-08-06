from .lagmat_func import lagmat
import numpy as np
import warnings


def diff_dth(x, order=1):
    """Differences of order d

    Parameters:
    -----------
    x : ndarray (2D)
        Time series with the oldest observation in the first row
        and the latest observation in the last row.

    order : int
        The number of differences to compute recursively
        (Default: 1 for I(1) processes.)

    Returns:
    --------
    y : ndarray (2D)
        The I(order=d) differences

    """
    y = np.array(x, copy=True, dtype=float)
    for i in range(order):
        y -= lagmat(y, lags=[1])
    return y


def diff_1st(x):
    """Difference x_t - x_{t-1} or Order of Integration I(1)

    Parameters:
    -----------
    x : ndarray (2D)
        Time series with the oldest observation in the first row
        and the latest observation in the last row.

    Returns:
    --------
    y : ndarray (2D)
        The I(1) differences x[1:, :] - x[:-1, :]

    Alternative Implementation:
    ---------------------------
        import numpy as np
        def diff_1st(x):
            y = np.empty(shape=x.shape)
            y[0, :] = np.nan
            y[1:, :] = x[1:, :] - x[:-1, :]
            return y
    """
    warnings.warn((
        "This function is for demonstration purpose only. "
        "It is equivalent to 'y = diff_dth(x, order=1)'. "
        "Please use 'diff_dth' instead."))
    return x - lagmat(x, lags=[1])
