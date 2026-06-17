"""Statistical estimators for dark-count analysis."""

import numpy as np


def dark_count_rate(n_events, live_time_s):
    """Estimate dark count rate and Poisson standard uncertainty."""
    if n_events <= 0:
        raise ValueError("n_events must be positive.")
    if live_time_s <= 0:
        raise ValueError("live_time_s must be positive.")
    rate_hz = n_events / live_time_s
    uncertainty_hz = np.sqrt(n_events) / live_time_s
    return rate_hz, uncertainty_hz


def rate_density_mhz_per_mm2(rate_hz, area_mm2=36.0):
    """Convert a rate in Hz to mHz/mm^2."""
    return np.asarray(rate_hz) * 1000.0 / area_mm2


def exponential_mle(interarrival_s):
    """Return the MLE rate for exponentially distributed inter-arrival times."""
    interarrival_s = np.asarray(interarrival_s, dtype=float)
    if np.any(interarrival_s <= 0):
        raise ValueError("Inter-arrival times must be positive.")
    mean_interval_s = np.mean(interarrival_s)
    rate_hz = 1.0 / mean_interval_s
    return rate_hz, mean_interval_s


def exponential_ks_test(interarrival_s):
    """Perform a one-sample KS check against an exponential model.

    The exponential scale is estimated from the same data, so this p-value is a
    classroom diagnostic rather than a rigorous final goodness-of-fit result.
    """
    interarrival_s = np.asarray(interarrival_s, dtype=float)
    _, scale_s = exponential_mle(interarrival_s)
    try:
        from scipy import stats
    except ImportError:
        statistic, pvalue = _exponential_ks_test_numpy(interarrival_s, scale_s)
        return statistic, pvalue

    statistic, pvalue = stats.kstest(interarrival_s, "expon", args=(0, scale_s))
    return statistic, pvalue


def _exponential_ks_test_numpy(interarrival_s, scale_s):
    """Small NumPy fallback for environments where SciPy is unavailable."""
    values = np.sort(interarrival_s)
    n = len(values)
    cdf = 1.0 - np.exp(-values / scale_s)
    empirical_upper = np.arange(1, n + 1) / n
    empirical_lower = np.arange(0, n) / n
    statistic = np.max(np.maximum(empirical_upper - cdf, cdf - empirical_lower))

    # Asymptotic Kolmogorov survival approximation. This is sufficient for the
    # teaching diagnostic, while SciPy remains the expected student tool.
    z = np.sqrt(n) * statistic
    terms = [(-1) ** (k - 1) * np.exp(-2 * k * k * z * z) for k in range(1, 101)]
    pvalue = min(max(2 * np.sum(terms), 0.0), 1.0)
    return float(statistic), float(pvalue)
