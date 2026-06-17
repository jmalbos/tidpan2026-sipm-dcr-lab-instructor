"""Shared pytest fixtures for the SiPM DCR lab."""

from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "massibo_example.npy"


@pytest.fixture
def tiny_events(tmp_path):
    """Create a tiny MASSIBO-like file with easy-to-check values."""
    timestamps = np.array([100, 110, 140, 200], dtype=np.uint64)
    waveforms = np.array(
        [
            [10, 10, 10, 7, 9],
            [20, 20, 20, 12, 19],
            [30, 30, 30, 28, 29],
            [40, 40, 40, 20, 39],
        ],
        dtype=np.uint64,
    )
    data = np.column_stack([timestamps, waveforms])
    path = tmp_path / "tiny_massibo.npy"
    np.save(path, data)
    return path, timestamps, waveforms


@pytest.fixture
def massibo_example_path():
    return DATA_PATH
