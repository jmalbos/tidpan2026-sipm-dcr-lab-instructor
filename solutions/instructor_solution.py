"""Instructor reference solution for the SiPM dark count rate lab."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from sipm_lab.classification import (
    burst_candidates,
    crosstalk_candidates,
    isolated_events,
    short_delay_candidates,
)
from sipm_lab.io import load_massibo_file, validate_timestamps
from sipm_lab.plotting import (
    plot_amplitude_histogram,
    plot_interarrival_histogram,
    plot_waveforms,
)
from sipm_lab.statistics import (
    dark_count_rate,
    exponential_ks_test,
    exponential_mle,
    rate_density_mhz_per_mm2,
)
from sipm_lab.timing import interarrival_times, live_time_seconds, ticks_to_seconds
from sipm_lab.waveforms import negative_pulse_amplitudes, negative_pulse_sample_indices


DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "massibo_example.npy"
SIPM_AREA_MM2 = 36.0


def analyze_file(path=DEFAULT_DATA_PATH):
    """Run the full reference analysis and return a results dictionary."""
    timestamps, waveforms = load_massibo_file(path)
    validate_timestamps(timestamps)

    times_s = ticks_to_seconds(timestamps)
    live_time_s = live_time_seconds(timestamps)
    intervals_s = interarrival_times(timestamps)
    rate_hz, rate_uncertainty_hz = dark_count_rate(len(timestamps), live_time_s)
    rate_density = rate_density_mhz_per_mm2(rate_hz, area_mm2=SIPM_AREA_MM2)
    rate_density_uncertainty = rate_density_mhz_per_mm2(
        rate_uncertainty_hz,
        area_mm2=SIPM_AREA_MM2,
    )
    exponential_rate_hz, mean_interval_s = exponential_mle(intervals_s)
    ks_statistic, ks_pvalue = exponential_ks_test(intervals_s)

    burst_mask = burst_candidates(times_s, dt_max_s=0.1, n_min=5)
    n_nonburst_events = int(np.sum(~burst_mask))
    clean_times_s = times_s[~burst_mask]
    clean_waveforms = waveforms[~burst_mask]
    clean_intervals_s = np.diff(clean_times_s)
    amplitudes = negative_pulse_amplitudes(clean_waveforms)
    pulse_indices = negative_pulse_sample_indices(clean_waveforms)

    burst_cleaned_rate_hz, burst_cleaned_rate_uncertainty_hz = dark_count_rate(
        n_nonburst_events,
        live_time_s,
    )
    burst_cleaned_rate_density = rate_density_mhz_per_mm2(
        burst_cleaned_rate_hz,
        area_mm2=SIPM_AREA_MM2,
    )
    burst_cleaned_rate_density_uncertainty = rate_density_mhz_per_mm2(
        burst_cleaned_rate_uncertainty_hz,
        area_mm2=SIPM_AREA_MM2,
    )

    crosstalk_mask, crosstalk_threshold = crosstalk_candidates(amplitudes)
    afterpulse_mask = short_delay_candidates(
        clean_intervals_s,
        min_delay_s=1e-6,
        max_delay_s=100e-6,
    )
    prompt_mask = short_delay_candidates(clean_intervals_s, min_delay_s=0.0, max_delay_s=10e-6)
    isolated_mask = isolated_events(
        clean_intervals_s,
        amplitudes,
        min_previous_delay_s=1e-3,
        max_amplitude=crosstalk_threshold,
    )

    return {
        "path": Path(path),
        "n_events": len(timestamps),
        "n_samples": waveforms.shape[1],
        "live_time_s": live_time_s,
        "rate_hz": rate_hz,
        "rate_uncertainty_hz": rate_uncertainty_hz,
        "rate_density_mhz_per_mm2": float(rate_density),
        "rate_density_uncertainty_mhz_per_mm2": float(rate_density_uncertainty),
        "sipm_area_mm2": SIPM_AREA_MM2,
        "n_burst_events": int(np.sum(burst_mask)),
        "n_nonburst_events": n_nonburst_events,
        "burst_cleaned_rate_hz": burst_cleaned_rate_hz,
        "burst_cleaned_rate_uncertainty_hz": burst_cleaned_rate_uncertainty_hz,
        "burst_cleaned_rate_density_mhz_per_mm2": float(burst_cleaned_rate_density),
        "burst_cleaned_rate_density_uncertainty_mhz_per_mm2": float(
            burst_cleaned_rate_density_uncertainty
        ),
        "mean_interarrival_s": mean_interval_s,
        "exponential_rate_hz": exponential_rate_hz,
        "ks_statistic": ks_statistic,
        "ks_pvalue": ks_pvalue,
        "amplitude_median_adc": float(np.median(amplitudes)),
        "amplitude_p95_adc": float(np.percentile(amplitudes, 95)),
        "amplitude_p99_adc": float(np.percentile(amplitudes, 99)),
        "pulse_index_median": float(np.median(pulse_indices)),
        "crosstalk_threshold_adc": float(crosstalk_threshold),
        "n_crosstalk_candidates": int(np.sum(crosstalk_mask)),
        "n_afterpulse_candidates": int(np.sum(afterpulse_mask)),
        "n_prompt_delay_candidates": int(np.sum(prompt_mask)),
        "n_isolated_events": int(np.sum(isolated_mask)),
        "timestamps": timestamps,
        "waveforms": waveforms,
        "interarrival_s": intervals_s,
        "clean_times_s": clean_times_s,
        "clean_waveforms": clean_waveforms,
        "clean_interarrival_s": clean_intervals_s,
        "amplitudes": amplitudes,
        "burst_mask": burst_mask,
        "crosstalk_mask": crosstalk_mask,
        "afterpulse_mask": afterpulse_mask,
        "prompt_mask": prompt_mask,
        "isolated_mask": isolated_mask,
    }


def print_summary(results):
    """Print a compact instructor-facing summary."""
    print(f"File: {results['path']}")
    print(f"Events: {results['n_events']}")
    print(f"Waveform samples per event: {results['n_samples']}")
    print(f"Live time: {results['live_time_s']:.6f} s")
    print(
        "Dark count rate: "
        f"{results['rate_hz']:.6f} +/- {results['rate_uncertainty_hz']:.6f} Hz"
    )
    print(
        "Dark count rate density: "
        f"{results['rate_density_mhz_per_mm2']:.3f} +/- "
        f"{results['rate_density_uncertainty_mhz_per_mm2']:.3f} mHz/mm^2"
    )
    print(f"Burst-tagged events, dt <= 100 ms and N >= 5: {results['n_burst_events']}")
    print(f"Non-burst events: {results['n_nonburst_events']}")
    print(
        "Burst-cleaned dark count rate: "
        f"{results['burst_cleaned_rate_hz']:.6f} +/- "
        f"{results['burst_cleaned_rate_uncertainty_hz']:.6f} Hz"
    )
    print(
        "Burst-cleaned dark count rate density: "
        f"{results['burst_cleaned_rate_density_mhz_per_mm2']:.3f} +/- "
        f"{results['burst_cleaned_rate_density_uncertainty_mhz_per_mm2']:.3f} mHz/mm^2"
    )
    print(f"Mean inter-arrival time: {results['mean_interarrival_s']:.6f} s")
    print(f"Exponential MLE rate: {results['exponential_rate_hz']:.6f} Hz")
    print(
        "KS diagnostic against exponential: "
        f"D = {results['ks_statistic']:.6f}, p = {results['ks_pvalue']:.6g}"
    )
    print(f"Median burst-cleaned pulse amplitude: {results['amplitude_median_adc']:.3f} ADC")
    print(f"95th percentile burst-cleaned amplitude: {results['amplitude_p95_adc']:.3f} ADC")
    print(f"99th percentile burst-cleaned amplitude: {results['amplitude_p99_adc']:.3f} ADC")
    print(f"Median burst-cleaned pulse sample index: {results['pulse_index_median']:.1f}")
    print(f"Crosstalk-like threshold: {results['crosstalk_threshold_adc']:.3f} ADC")
    print(f"Burst-cleaned crosstalk-like candidates: {results['n_crosstalk_candidates']}")
    print(f"Burst-cleaned afterpulse-like candidates, 1-100 us: {results['n_afterpulse_candidates']}")
    print(f"Burst-cleaned prompt short-delay candidates, <=10 us: {results['n_prompt_delay_candidates']}")
    print(f"Burst-cleaned isolated dark-count-like events: {results['n_isolated_events']}")


def make_plots(results):
    """Create the standard instructor solution plots."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    plot_waveforms(axes[0], results["clean_waveforms"], n=10)
    plot_interarrival_histogram(
        axes[1],
        results["clean_interarrival_s"],
        rate_hz=results["burst_cleaned_rate_hz"],
        bins=50,
    )
    plot_amplitude_histogram(
        axes[2],
        results["amplitudes"],
        threshold=results["crosstalk_threshold_adc"],
        bins=50,
    )
    fig.tight_layout()
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=DEFAULT_DATA_PATH, type=Path)
    parser.add_argument("--show-plots", action="store_true")
    args = parser.parse_args()

    results = analyze_file(args.path)
    print_summary(results)
    if args.show_plots:
        import matplotlib.pyplot as plt

        make_plots(results)
        plt.show()


if __name__ == "__main__":
    main()
