"""Tests for dark count rate calculations."""

import pytest

from student import analysis


def test_compute_dark_count_rate_and_uncertainty():
    rate_hz, uncertainty_hz = analysis.compute_dark_count_rate(n_events=100, live_time_s=20.0)

    assert rate_hz == pytest.approx(5.0)
    assert uncertainty_hz == pytest.approx(0.5)


def test_convert_rate_to_mhz_per_mm2():
    assert analysis.convert_rate_to_mhz_per_mm2(1.8, area_mm2=36.0) == pytest.approx(50.0)


def test_real_massibo_dark_count_rate(massibo_example_path):
    timestamps, _ = analysis.load_data(massibo_example_path)
    times_s = analysis.timestamps_to_seconds(timestamps)
    live_time_s = analysis.compute_live_time(times_s)

    rate_hz, uncertainty_hz = analysis.compute_dark_count_rate(len(timestamps), live_time_s)

    assert rate_hz == pytest.approx(1.7911078378695413)
    assert uncertainty_hz == pytest.approx(0.06251009455023479)

    rate_density = analysis.convert_rate_to_mhz_per_mm2(rate_hz, area_mm2=36.0)
    uncertainty_density = analysis.convert_rate_to_mhz_per_mm2(uncertainty_hz, area_mm2=36.0)

    assert rate_density == pytest.approx(49.752995496376146)
    assert uncertainty_density == pytest.approx(1.7363915152842997)
