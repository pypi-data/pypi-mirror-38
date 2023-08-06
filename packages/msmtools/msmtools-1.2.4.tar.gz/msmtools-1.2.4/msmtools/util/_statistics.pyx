import numpy as np
from cython.parallel import prange

def _maxlength(X):
    """ Returns the maximum length of signal trajectories X """
    return np.fromiter((map(lambda x: len(x), X)), dtype=int).max()


def statistical_inefficiency(X, truncate_acf=True, mact=1.0):
    """ Estimates the statistical inefficiency from univariate time series X

    The statistical inefficiency [1]_ is a measure of the correlatedness of samples in a signal.
    Given a signal :math:`{x_t}` with :math:`N` samples and statistical inefficiency :math:`I \in (0,1]`, there are
    only :math:`I \cdot N` effective or uncorrelated samples in the signal. This means that :math:`I \cdot N` should
    be used in order to compute statistical uncertainties. See [2]_ for a review.

    The statistical inefficiency is computed as :math:`I = (2 \tau)^{-1}` using the damped autocorrelation time

    .. math:
        \tau = \frac{1}{2}+\sum_{K=1}^{N} A(k) \left(1-\frac{k}{N}\right)

    where

    .. math:
        A(k) = \frac{\langle x_t x_{t+k} \rangle_t - \langle x^2 \rangle_t}{\mathrm{var}(x)}

    is the autocorrelation function of the signal :math:`{x_t}`, which is computed either for a single or multiple
    trajectories.

    Parameters
    ----------
    X : float array or list of float arrays
        Univariate time series (single or multiple trajectories)
    truncate_acf : bool, optional, default=True
        When the normalized autocorrelation function passes through 0, it is truncated in order to avoid integrating
        random noise

    References
    ----------
    .. [1] Anderson, T. W.: The Statistical Analysis of Time Series (Wiley, New York, 1971)

    .. [2] Janke, W: Statistical Analysis of Simulations: Data Correlations and Error Estimation
        Quantum Simulations of Complex Many-Body Systems: From Theory to Algorithms, Lecture Notes,
        J. Grotendorst, D. Marx, A. Muramatsu (Eds.), John von Neumann Institute for Computing, Juelich
        NIC Series 10, pp. 423-445, 2002.

    """
    # check input
    assert np.ndim(X[0]) == 1, 'Data must be 1-dimensional'
    cdef size_t N = _maxlength(X)  # max length
    # mean-free data
    xflat = np.concatenate(X)
    Xmean = np.mean(xflat)
    X0 = [x-Xmean for x in X]
    # moments
    x2m = np.mean(xflat ** 2)
    del xflat, Xmean
    # integrate damped autocorrelation
    corrsum = 0.0
    #cdef double acf
    #cdef size_t n
    for lag in prange(N, nogil=True):
        with gil:
            acf = 0.0
            n = 0
            # cache partial sums
            for x in X0:
                Nx = len(x)  # length of this trajectory
                if Nx > lag:  # only use trajectories that are long enough
                    prod = x[:Nx-lag] * x[lag:]
                    acf += np.sum(prod)
                    n += Nx-lag
            acf /= 1.0 * n
            if True:
                if acf <= 0 and truncate_acf:  # zero autocorrelation. Exit
                    break
                elif lag > 0:  # start integrating at lag 1 (effect of lag 0 is contained in the 0.5 below
                    corrsum += acf * (1.0 - (float(lag)/float(N)))
    # compute damped correlation time
    corrtime = 0.5 + mact * corrsum / x2m
    # return statistical inefficiency
    return 1.0 / (2 * corrtime)
