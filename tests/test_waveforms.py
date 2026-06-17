"""Tests for baseline and amplitude extraction."""

import numpy as np
import pytest

from student import analysis


def test_estimate_baseline_uses_pretrigger_median(tiny_events):
    _, _, waveforms = tiny_events

    baselines = analysis.estimate_baseline(waveforms, n_pretrigger=3)

    np.testing.assert_allclose(baselines, [10, 20, 30, 40])


def test_compute_negative_amplitudes(tiny_events):
    _, _, waveforms = tiny_events

    amplitudes = analysis.compute_negative_amplitudes(waveforms, n_pretrigger=3)

    np.testing.assert_allclose(amplitudes, [3, 8, 2, 20])


def test_real_massibo_amplitude_summary(massibo_example_path):
    timestamps, waveforms = analysis.load_data(massibo_example_path)
    times_s = analysis.timestamps_to_seconds(timestamps)
    burst_mask = analysis.tag_burst_events(times_s, dt_max_s=0.1, n_min=5)

    amplitudes = analysis.compute_negative_amplitudes(waveforms[~burst_mask], n_pretrigger=40)

    assert np.median(amplitudes) == 13
    assert np.percentile(amplitudes, 95) == 38
    assert np.percentile(amplitudes, 99) == pytest.approx(171.69)
