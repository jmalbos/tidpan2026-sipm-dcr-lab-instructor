"""Instructor answer key for `student/analysis.py`.

This file mirrors the student-facing function signatures so instructors can
compare directly against the expected implementations.
"""

from pathlib import Path

import numpy as np


TICK_SECONDS = 16e-9


def load_data(path):
    """Load one MASSIBO `.npy` file."""
    data = np.load(Path(path))
    return data[:, 0], data[:, 1:]


def timestamps_to_seconds(timestamps, tick_seconds=TICK_SECONDS):
    """Convert raw timestamp ticks to seconds."""
    return np.asarray(timestamps, dtype=float) * tick_seconds


def compute_live_time(times_s):
    """Compute acquisition live time from event times in seconds."""
    times_s = np.asarray(times_s, dtype=float)
    return times_s[-1] - times_s[0]


def compute_interarrival_times(times_s):
    """Compute event-to-event inter-arrival times in seconds."""
    return np.diff(np.asarray(times_s, dtype=float))


def compute_dark_count_rate(n_events, live_time_s):
    """Estimate the dark count rate and Poisson standard uncertainty."""
    rate_hz = n_events / live_time_s
    uncertainty_hz = np.sqrt(n_events) / live_time_s
    return rate_hz, uncertainty_hz


def convert_rate_to_mhz_per_mm2(rate_hz, area_mm2=36.0):
    """Convert a rate in Hz to mHz/mm^2."""
    return np.asarray(rate_hz) * 1000.0 / area_mm2


def tag_burst_events(times_s, dt_max_s=0.1, n_min=5):
    """Return a boolean mask for events belonging to burst candidates."""
    times_s = np.asarray(times_s, dtype=float)
    intervals_s = np.diff(times_s)
    burst_mask = np.zeros(len(times_s), dtype=bool)

    i = 0
    while i < len(intervals_s):
        if intervals_s[i] <= dt_max_s:
            start = i
            while i < len(intervals_s) and intervals_s[i] <= dt_max_s:
                i += 1
            stop = i
            n_events = stop - start + 1
            if n_events >= n_min:
                burst_mask[start : stop + 1] = True
        else:
            i += 1

    return burst_mask


def estimate_baseline(waveforms, n_pretrigger=40):
    """Estimate one baseline value per waveform using pre-trigger samples."""
    waveforms = np.asarray(waveforms)
    return np.median(waveforms[:, :n_pretrigger], axis=1)


def compute_negative_amplitudes(waveforms, n_pretrigger=40):
    """Compute baseline-subtracted amplitudes for negative-going pulses."""
    waveforms = np.asarray(waveforms)
    baselines = estimate_baseline(waveforms, n_pretrigger=n_pretrigger)
    minima = np.min(waveforms, axis=1)
    return baselines - minima


def tag_crosstalk_candidates(amplitudes, threshold_adc):
    """Return a boolean mask for high-amplitude crosstalk-like candidates."""
    return np.asarray(amplitudes) >= threshold_adc


def tag_afterpulse_candidates(interarrival_s, min_delay_s=1e-6, max_delay_s=100e-6):
    """Return a boolean event mask for short-delay afterpulse-like candidates."""
    interarrival_s = np.asarray(interarrival_s)
    interval_mask = (interarrival_s >= min_delay_s) & (interarrival_s <= max_delay_s)
    event_mask = np.zeros(len(interarrival_s) + 1, dtype=bool)
    event_mask[1:] = interval_mask
    return event_mask


def summarize_results(n_events, live_time_s, rate_hz, uncertainty_hz):
    """Create a compact text summary for the notebook."""
    return (
        f"Events: {n_events}\n"
        f"Live time: {live_time_s:.3f} s\n"
        f"Dark count rate: {rate_hz:.3f} +/- {uncertainty_hz:.3f} Hz"
    )
