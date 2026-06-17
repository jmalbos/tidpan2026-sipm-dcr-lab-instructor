"""Plotting helpers for the student notebook and reference analysis."""

import numpy as np

from sipm_lab import SAMPLE_SECONDS


def plot_waveforms(ax, waveforms, n=10, sample_seconds=SAMPLE_SECONDS):
    """Plot the first `n` waveforms on an existing Matplotlib axis."""
    waveforms = np.asarray(waveforms)
    time_us = np.arange(waveforms.shape[1]) * sample_seconds * 1e6
    for waveform in waveforms[:n]:
        ax.plot(time_us, waveform, alpha=0.7)
    ax.set_xlabel("time within waveform [us]")
    ax.set_ylabel("ADC counts")
    ax.set_title(f"First {min(n, len(waveforms))} waveforms")
    return ax


def plot_interarrival_histogram(ax, interarrival_s, rate_hz, bins=50):
    """Plot inter-arrival times with the exponential expectation."""
    interarrival_s = np.asarray(interarrival_s)
    counts, edges, _ = ax.hist(interarrival_s, bins=bins, density=True, alpha=0.7)
    x = np.linspace(edges[0], edges[-1], 400)
    ax.plot(x, rate_hz * np.exp(-rate_hz * x), color="black", lw=2)
    ax.set_xlabel("inter-arrival time [s]")
    ax.set_ylabel("probability density")
    ax.set_title("Inter-arrival time distribution")
    return counts, edges


def plot_amplitude_histogram(ax, amplitudes, threshold=None, bins=50):
    """Plot pulse amplitudes and optionally mark a crosstalk-like threshold."""
    ax.hist(amplitudes, bins=bins, alpha=0.7)
    if threshold is not None:
        ax.axvline(threshold, color="black", linestyle="--", label="threshold")
        ax.legend()
    ax.set_xlabel("negative pulse amplitude [ADC counts]")
    ax.set_ylabel("events")
    ax.set_title("Pulse amplitude distribution")
    return ax
