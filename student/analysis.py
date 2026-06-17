"""Student-facing functions for the SiPM dark count rate lab.

Complete the TODO sections during the lab. Keep the function signatures fixed:
the notebook and automated tests call these functions directly.
"""

from pathlib import Path

import numpy as np


TICK_SECONDS = 16e-9


def load_data(path):
    """Load one MASSIBO `.npy` file.

    Parameters
    ----------
    path:
        Path to the data file. The file contains one 2D NumPy array.

    Returns
    -------
    timestamps:
        One timestamp per event, in raw 62.5 MHz clock ticks.
    waveforms:
        ADC waveform samples. Shape: (n_events, n_samples).
    """
    # TODO: load the array with np.load, then split column 0 from the ADC samples.
    # Hint: timestamps are in data[:, 0], waveforms are in data[:, 1:].
    raise NotImplementedError


def timestamps_to_seconds(timestamps, tick_seconds=TICK_SECONDS):
    """Convert raw timestamp ticks to seconds."""
    # TODO: multiply timestamps by the tick duration.
    raise NotImplementedError


def compute_live_time(times_s):
    """Compute acquisition live time from event times in seconds."""
    # TODO: use the time span between the last and first event.
    # Do not assume that the acquisition lasted exactly 10 minutes.
    raise NotImplementedError


def compute_interarrival_times(times_s):
    """Compute event-to-event inter-arrival times in seconds."""
    # TODO: compute the difference between consecutive event times.
    raise NotImplementedError


def compute_dark_count_rate(n_events, live_time_s):
    """Estimate the dark count rate and Poisson standard uncertainty.

    Returns
    -------
    rate_hz:
        Estimated event rate in Hz.
    uncertainty_hz:
        Poisson standard uncertainty on the rate.
    """
    # TODO: rate = n_events / live_time_s
    # TODO: uncertainty = sqrt(n_events) / live_time_s
    raise NotImplementedError


def convert_rate_to_mhz_per_mm2(rate_hz, area_mm2=36.0):
    """Convert a rate in Hz to mHz/mm^2."""
    # TODO: multiply by 1000 to convert Hz to mHz, then divide by area_mm2.
    raise NotImplementedError


def tag_burst_events(times_s, dt_max_s=0.1, n_min=5):
    """Return a boolean mask for events belonging to burst candidates.

    A burst candidate is a sequence of at least n_min consecutive events where
    each neighboring pair is separated by no more than dt_max_s.
    """
    # TODO: find runs of consecutive inter-arrival times <= dt_max_s.
    # A run of k short intervals corresponds to k + 1 events.
    raise NotImplementedError


def estimate_baseline(waveforms, n_pretrigger=40):
    """Estimate one baseline value per waveform using pre-trigger samples."""
    # TODO: use the median of the first n_pretrigger samples for each waveform.
    raise NotImplementedError


def compute_negative_amplitudes(waveforms, n_pretrigger=40):
    """Compute baseline-subtracted amplitudes for negative-going pulses."""
    # TODO: estimate the baseline, find each waveform minimum, and subtract.
    # For negative-going pulses: amplitude = baseline - minimum_adc.
    raise NotImplementedError


def tag_crosstalk_candidates(amplitudes, threshold_adc):
    """Return a boolean mask for high-amplitude crosstalk-like candidates."""
    # TODO: mark events with amplitude greater than or equal to threshold_adc.
    raise NotImplementedError


def tag_afterpulse_candidates(interarrival_s, min_delay_s=1e-6, max_delay_s=100e-6):
    """Return a boolean event mask for short-delay afterpulse-like candidates.

    The returned mask should have one entry per event. The first event has no
    previous inter-arrival time, so it should always be False.
    """
    # TODO: identify inter-arrival times inside the requested delay window.
    # Hint: interarrival_s has length n_events - 1.
    raise NotImplementedError


def summarize_results(n_events, live_time_s, rate_hz, uncertainty_hz):
    """Create a compact text summary for the notebook."""
    return (
        f"Events: {n_events}\n"
        f"Live time: {live_time_s:.3f} s\n"
        f"Dark count rate: {rate_hz:.3f} +/- {uncertainty_hz:.3f} Hz"
    )
