"""Tests for loading MASSIBO data."""

import numpy as np

from student import analysis


def test_load_data_splits_timestamps_and_waveforms(tiny_events):
    path, expected_timestamps, expected_waveforms = tiny_events

    timestamps, waveforms = analysis.load_data(path)

    np.testing.assert_array_equal(timestamps, expected_timestamps)
    np.testing.assert_array_equal(waveforms, expected_waveforms)


def test_load_real_massibo_file_shape(massibo_example_path):
    timestamps, waveforms = analysis.load_data(massibo_example_path)

    assert timestamps.shape == (821,)
    assert waveforms.shape == (821, 251)
    assert np.all(np.diff(timestamps) > 0)
