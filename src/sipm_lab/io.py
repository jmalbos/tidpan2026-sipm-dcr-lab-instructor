"""Input/output helpers for MASSIBO NumPy files."""

from pathlib import Path

import numpy as np


def load_massibo_file(path):
    """Load one MASSIBO `.npy` file and return timestamps and waveforms.

    Parameters
    ----------
    path:
        Path to a NumPy array where column 0 is the trigger timestamp and the
        remaining columns are waveform ADC samples.
    """
    data = np.load(Path(path))
    if data.ndim != 2:
        raise ValueError(f"Expected a 2D array, got shape {data.shape}.")
    if data.shape[1] < 2:
        raise ValueError("Expected at least one timestamp column and one ADC sample.")

    timestamps = data[:, 0]
    waveforms = data[:, 1:]
    return timestamps, waveforms


def validate_timestamps(timestamps):
    """Check that event timestamps are sorted and unique."""
    timestamps = np.asarray(timestamps)
    if timestamps.ndim != 1:
        raise ValueError("Timestamps must be a one-dimensional array.")
    if len(timestamps) < 2:
        raise ValueError("At least two timestamps are required.")

    differences = np.diff(timestamps)
    if np.any(differences < 0):
        raise ValueError("Timestamps must be sorted in nondecreasing order.")
    if np.any(differences == 0):
        raise ValueError("Duplicate timestamps found.")

    return True
