"""Waveform baseline and amplitude helpers."""

import numpy as np


def estimate_baseline(waveforms, n_pretrigger=40):
    """Estimate one baseline value per waveform using early samples."""
    waveforms = np.asarray(waveforms)
    if waveforms.ndim != 2:
        raise ValueError("Waveforms must be a two-dimensional array.")
    if not 1 <= n_pretrigger <= waveforms.shape[1]:
        raise ValueError("n_pretrigger must be within the waveform length.")
    return np.median(waveforms[:, :n_pretrigger], axis=1)


def negative_pulse_amplitudes(waveforms, n_pretrigger=40):
    """Return baseline-subtracted amplitudes for negative-going pulses."""
    waveforms = np.asarray(waveforms)
    baselines = estimate_baseline(waveforms, n_pretrigger=n_pretrigger)
    minima = np.min(waveforms, axis=1)
    return baselines - minima


def negative_pulse_sample_indices(waveforms):
    """Return the sample index of the minimum ADC value in each waveform."""
    return np.argmin(np.asarray(waveforms), axis=1)


def find_negative_peaks(waveform, prominence=5):
    """Find negative-going peaks in one waveform using SciPy."""
    from scipy.signal import find_peaks

    waveform = np.asarray(waveform)
    peaks, properties = find_peaks(-waveform, prominence=prominence)
    return peaks, properties
