"""Tests for timestamp conversion and timing calculations."""

import numpy as np
import pytest

from student import analysis


def test_timestamps_to_seconds_uses_16_ns_ticks():
    timestamps = np.array([0, 1, 10, 100], dtype=np.uint64)

    times_s = analysis.timestamps_to_seconds(timestamps)

    np.testing.assert_allclose(times_s, [0.0, 16e-9, 160e-9, 1600e-9])


def test_compute_live_time_uses_first_and_last_event():
    times_s = np.array([10.0, 11.5, 14.0, 20.0])

    live_time_s = analysis.compute_live_time(times_s)

    assert live_time_s == pytest.approx(10.0)


def test_compute_interarrival_times():
    times_s = np.array([10.0, 11.5, 14.0, 20.0])

    interarrival_s = analysis.compute_interarrival_times(times_s)

    np.testing.assert_allclose(interarrival_s, [1.5, 2.5, 6.0])


def test_real_massibo_live_time(massibo_example_path):
    timestamps, _ = analysis.load_data(massibo_example_path)
    times_s = analysis.timestamps_to_seconds(timestamps)

    live_time_s = analysis.compute_live_time(times_s)

    assert live_time_s == pytest.approx(458.375527504)
