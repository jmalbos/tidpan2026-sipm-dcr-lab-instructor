"""Timing conversions and inter-arrival-time helpers."""

import numpy as np

from sipm_lab import TICK_SECONDS


def ticks_to_seconds(timestamps, tick_seconds=TICK_SECONDS):
    """Convert MASSIBO clock ticks to seconds."""
    return np.asarray(timestamps, dtype=float) * tick_seconds


def live_time_seconds(timestamps, tick_seconds=TICK_SECONDS):
    """Compute acquisition live time from first and last timestamp."""
    times = ticks_to_seconds(timestamps, tick_seconds=tick_seconds)
    if len(times) < 2:
        raise ValueError("At least two timestamps are required to compute live time.")
    live_time = times[-1] - times[0]
    if live_time <= 0:
        raise ValueError("Live time must be positive.")
    return live_time


def interarrival_times(timestamps, tick_seconds=TICK_SECONDS):
    """Compute event-to-event inter-arrival times in seconds."""
    times = ticks_to_seconds(timestamps, tick_seconds=tick_seconds)
    intervals = np.diff(times)
    if np.any(intervals <= 0):
        raise ValueError("Inter-arrival times must be positive.")
    return intervals
