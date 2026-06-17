# SiPM Dark Count Rate Lab

## Context

Silicon photomultipliers, or SiPMs, are compact photon detectors used in many
particle-physics experiments. In this exercise you will analyze real data from
MASSIBO, a setup used for large-scale SiPM characterization in the context of
the DUNE experiment.

The data were acquired at liquid-nitrogen temperature. At this temperature the
dark count rate is strongly reduced compared with room temperature, but random
dark counts and correlated noise can still be observed.

## Learning Goals

By the end of the lab, you should be able to:

- load MASSIBO waveform-trigger data stored in NumPy format,
- convert clock ticks into physical time,
- estimate a dark count rate and its Poisson uncertainty,
- identify burst candidates using consecutive short inter-arrival times,
- quote dark count rates in Hz and mHz/mm^2,
- compare inter-arrival times with an exponential expectation,
- extract a simple pulse amplitude from negative-going waveforms,
- tag simple crosstalk-like and afterpulse-like candidate events,
- explain why real detector data may deviate from an ideal Poisson model.

## Files You Will Use

```text
data/massibo_example.npy
notebooks/01_sipm_dark_counts.ipynb
student/analysis.py
tests/
```

Edit `student/analysis.py`. The notebook calls those functions, and the tests
check the same functions.

## Data Format

The `.npy` file contains one two-dimensional array. Each row is one trigger for
one SiPM sensor.

```text
column 0      event timestamp in 62.5 MHz clock ticks
columns 1:    ADC waveform samples
```

Timing convention:

```text
1 tick = 16 ns
1 waveform sample = 16 ns
251 samples = about 4 us
```

The pulses in this dataset are negative-going.

## Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Start Jupyter:

```bash
jupyter lab
```

Open:

```text
notebooks/01_sipm_dark_counts.ipynb
```

You can run tests with:

```bash
pytest
```

## Task 1: Load The Data

Implement `load_data(path)`.

It should return:

```text
timestamps      raw timestamp ticks
waveforms       ADC samples, shape (n_events, n_samples)
```

Checkpoint:

- How many events are in the file?
- How many waveform samples does each event contain?

## Task 2: Convert Timestamps

Implement:

```text
timestamps_to_seconds
compute_live_time
compute_interarrival_times
```

Use the timestamp conversion:

```text
time_s = timestamp * 16e-9
```

The acquisition may have stopped before 10 minutes. Estimate the live time from
the first and last timestamp.

Checkpoint:

- What is the live time of the example file?
- Why should you not assume exactly 10 minutes?

## Task 3: Dark Count Rate

Implement:

```text
compute_dark_count_rate
convert_rate_to_mhz_per_mm2
```

Use:

```text
rate = N / T
sigma_rate = sqrt(N) / T
```

where `N` is the number of events and `T` is the live time.

The SiPM active area is:

```text
6 mm x 6 mm = 36 mm^2
```

Convert rates using:

```text
DCR [mHz/mm^2] = DCR [Hz] * 1000 / 36
```

Checkpoint:

- Report the dark count rate in Hz.
- Report the dark count rate in mHz/mm^2.
- Report the statistical uncertainty in both units.
- What assumptions are implicit in this uncertainty estimate?

## Task 4: Burst Tagging

MASSIBO data may include bursts: groups of many consecutive events separated by
short time intervals. In the DUNE-style tag method, an event sequence is tagged
as burst-like if it satisfies:

```text
dt <= 100 ms between neighboring events
N_events >= 5 in the sequence
```

Implement:

```text
tag_burst_events
```

Then compute the burst-cleaned DCR by removing burst-tagged events from the
event count. Use the burst-cleaned sample for the remaining amplitude,
crosstalk-like, and afterpulse-like candidate studies.

Checkpoint:

- How many events are tagged as burst-like?
- What is the burst-cleaned DCR in Hz?
- What is the burst-cleaned DCR in mHz/mm^2?
- Why is this different from tagging an afterpulse?

## Task 5: Inter-Arrival Times

Plot the inter-arrival-time distribution in the notebook.

For an ideal Poisson process, the inter-arrival-time distribution is exponential:

```text
p(dt) = rate * exp(-rate * dt)
```

Checkpoint:

- Where does the exponential model describe the data reasonably well?
- Where does it fail?
- What physical effects can produce an excess of short inter-arrival times?

## Task 6: Burst-Cleaned Waveform Amplitudes

Implement:

```text
estimate_baseline
compute_negative_amplitudes
```

Use the first pre-trigger samples to estimate the baseline. Since the pulses are
negative-going:

```text
amplitude = baseline - minimum_adc
```

Checkpoint:

- How many burst-cleaned waveforms remain?
- What is the typical pulse amplitude?
- Are there events with unusually large amplitudes?

## Task 7: Candidate Correlated Noise Tags

Implement:

```text
tag_crosstalk_candidates
tag_afterpulse_candidates
```

Use the burst-cleaned sample and the notebook thresholds:

```text
crosstalk-like: amplitude >= 2.5 * median_amplitude
afterpulse-like: previous inter-arrival time between 1 us and 100 us
```

These are simple candidate tags, not final detector-quality classifications.

Checkpoint:

- How many crosstalk-like candidates do you find?
- How many afterpulse-like candidates do you find?
- How do these counts change if you move the thresholds?

## Final Questions

Answer briefly:

1. What raw dark count rate did you measure?
2. What burst-cleaned dark count rate did you measure?
3. Does the dataset look like a pure Poisson process?
4. Which burst-cleaned observables suggest correlated noise?
5. How could temperature, overvoltage, threshold, or electronics dead time affect
   this analysis?
6. What would you change if you had to compare several SiPMs fairly?

## Quick Troubleshooting

If the notebook cannot import `student.analysis`, make sure Jupyter was started
from this repository or restart the kernel after installing the package.

If `pytest` is not found, activate the virtual environment:

```bash
source .venv/bin/activate
```

If the rate is extremely small or extremely large, check whether timestamps were
converted from ticks to seconds.

If amplitudes are negative, check the pulse polarity. These waveforms are
negative-going, so use `baseline - minimum_adc`.

If the afterpulse mask has the wrong length, remember that inter-arrival times
have one fewer entry than events. The first event has no previous delay.
