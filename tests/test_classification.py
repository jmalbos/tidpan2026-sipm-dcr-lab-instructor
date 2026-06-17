"""Tests for simple correlated-event candidate tags."""

import numpy as np

from student import analysis


def test_tag_crosstalk_candidates():
    amplitudes = np.array([10, 12, 30, 40, 9])

    mask = analysis.tag_crosstalk_candidates(amplitudes, threshold_adc=30)

    np.testing.assert_array_equal(mask, [False, False, True, True, False])


def test_tag_afterpulse_candidates_returns_event_mask():
    interarrival_s = np.array([0.5, 5e-6, 2e-4, 80e-6])

    mask = analysis.tag_afterpulse_candidates(
        interarrival_s,
        min_delay_s=1e-6,
        max_delay_s=100e-6,
    )

    np.testing.assert_array_equal(mask, [False, False, True, False, True])


def test_tag_burst_events_requires_minimum_cluster_size():
    times_s = np.array([0.0, 0.05, 0.10, 0.15, 0.20, 1.0, 1.05, 1.10])

    mask = analysis.tag_burst_events(times_s, dt_max_s=0.1, n_min=5)

    np.testing.assert_array_equal(mask, [True, True, True, True, True, False, False, False])


def test_real_massibo_candidate_counts(massibo_example_path):
    timestamps, waveforms = analysis.load_data(massibo_example_path)
    times_s = analysis.timestamps_to_seconds(timestamps)
    burst_mask = analysis.tag_burst_events(times_s, dt_max_s=0.1, n_min=5)
    clean_times_s = times_s[~burst_mask]
    clean_waveforms = waveforms[~burst_mask]
    clean_interarrival_s = analysis.compute_interarrival_times(clean_times_s)
    amplitudes = analysis.compute_negative_amplitudes(clean_waveforms, n_pretrigger=40)

    crosstalk_threshold_adc = 2.5 * np.median(amplitudes)
    crosstalk_mask = analysis.tag_crosstalk_candidates(amplitudes, crosstalk_threshold_adc)
    afterpulse_mask = analysis.tag_afterpulse_candidates(
        clean_interarrival_s,
        min_delay_s=1e-6,
        max_delay_s=100e-6,
    )

    assert crosstalk_threshold_adc == 32.5
    assert np.sum(burst_mask) == 289
    assert np.sum(~burst_mask) == 532
    assert np.sum(crosstalk_mask) == 34
    assert np.sum(afterpulse_mask) == 15
