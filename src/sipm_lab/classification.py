"""Simple rule-based tags for correlated event candidates."""

import numpy as np


def crosstalk_candidates(amplitudes, threshold=None, multiplier=2.5):
    """Tag high-amplitude pulses as crosstalk-like candidates."""
    amplitudes = np.asarray(amplitudes, dtype=float)
    if threshold is None:
        threshold = multiplier * np.median(amplitudes)
    return amplitudes >= threshold, threshold


def short_delay_candidates(interarrival_s, min_delay_s=1e-6, max_delay_s=100e-6):
    """Tag events preceded by a short inter-arrival time.

    Returns a mask with one entry per event. The first event is always false
    because it has no previous inter-arrival time.
    """
    interarrival_s = np.asarray(interarrival_s, dtype=float)
    short_intervals = (interarrival_s >= min_delay_s) & (interarrival_s <= max_delay_s)
    event_mask = np.zeros(len(interarrival_s) + 1, dtype=bool)
    event_mask[1:] = short_intervals
    return event_mask


def burst_candidates(times_s, dt_max_s=0.1, n_min=5):
    """Tag events in burst candidates using consecutive short intervals."""
    times_s = np.asarray(times_s, dtype=float)
    intervals_s = np.diff(times_s)
    event_mask = np.zeros(len(times_s), dtype=bool)

    i = 0
    while i < len(intervals_s):
        if intervals_s[i] <= dt_max_s:
            start = i
            while i < len(intervals_s) and intervals_s[i] <= dt_max_s:
                i += 1
            stop = i
            n_events = stop - start + 1
            if n_events >= n_min:
                event_mask[start : stop + 1] = True
        else:
            i += 1

    return event_mask


def isolated_events(interarrival_s, amplitudes, min_previous_delay_s=1e-3, max_amplitude=None):
    """Tag ordinary isolated events using simple timing and amplitude cuts."""
    interarrival_s = np.asarray(interarrival_s, dtype=float)
    amplitudes = np.asarray(amplitudes, dtype=float)
    if len(amplitudes) != len(interarrival_s) + 1:
        raise ValueError("Need one more amplitude than inter-arrival time.")
    if max_amplitude is None:
        max_amplitude = 2.5 * np.median(amplitudes)

    mask = np.ones(len(amplitudes), dtype=bool)
    mask[1:] &= interarrival_s >= min_previous_delay_s
    mask &= amplitudes < max_amplitude
    return mask
