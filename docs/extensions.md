# Extension Exercises

These exercises are optional. They are useful for fast students, longer
sessions, or follow-up projects.

## Extension 1: Crosstalk Threshold Scan

Vary the crosstalk-like amplitude threshold:

```text
threshold = k * median_amplitude
```

Try:

```text
k = 1.5, 2.0, 2.5, 3.0, 4.0
```

Plot candidate count versus `k`.

Questions:

- Does the count change smoothly?
- Is there an obvious separation between ordinary pulses and high-amplitude
  candidates?
- Why is this not yet a calibrated crosstalk probability?
- Do the scan on the burst-cleaned sample. How different is it if burst events
  are included?

## Extension 2: Afterpulse Time-Window Scan

Change the afterpulse-like delay window using the burst-cleaned inter-arrival
times.

Suggested windows:

```text
1-10 us
10-50 us
50-100 us
100-500 us
```

Questions:

- Which window contains the most candidates?
- How does the result compare with the inter-arrival-time histogram?
- What detector or electronics effects could mimic short-delay correlations?

## Extension 3: Rate After Removing Candidate Correlated Events

Starting from the burst-cleaned sample, compare the DCR before and after
removing crosstalk-like or afterpulse-like candidates.

Questions:

- How much does the rate change?
- Is this corrected rate necessarily a better estimate of the primary dark
  count rate?
- Which assumptions are required for this correction to be meaningful?

## Extension 4: Burst Parameter Scan

Repeat the burst tagging while varying:

```text
dt_max = 10 ms, 50 ms, 100 ms, 200 ms
n_min = 3, 5, 10
```

Questions:

- Which parameter has the larger effect on the cleaned DCR?
- Are all tagged bursts visually obvious in the inter-arrival-time plot?
- Why did the DUNE-style criterion choose a large time window but require
  several consecutive events?

## Extension 5: Compare Two Sensors Or Runs

If an additional MASSIBO file is available, repeat the analysis for a second
sensor or run.

Compare:

- live time,
- dark count rate,
- amplitude distribution,
- short-delay candidate counts.

Questions:

- What metadata would you need for a fair comparison?
- Could different thresholds, gains, or overvoltages explain differences?
- What should be normalized before comparing sensors?

## Extension 6: Exponential Model Diagnostics

Use `scipy.stats` to compare the measured inter-arrival times to an exponential
model.

Possible tools:

```text
scipy.stats.kstest
scipy.stats.expon.fit
```

Questions:

- What happens if you exclude very short inter-arrival times before fitting?
- Does the fitted rate change?
- Why should a p-value be interpreted carefully when model parameters are
  estimated from the same data?

## Extension 7: Waveform-Level Peak Finding

Use `scipy.signal.find_peaks` on `-waveform` to identify negative-going peaks.

Try changing:

```text
prominence
distance
height
```

Questions:

- How often do you find more than one peak in a waveform?
- Are multi-peak waveforms associated with short inter-arrival times?
- How sensitive are the results to the peak-finding settings?

## Extension 8: Uncertainty Beyond Counting Statistics

The lab uses:

```text
sigma_rate = sqrt(N) / T
```

Discuss additional sources of uncertainty:

- threshold choice,
- live-time definition,
- baseline estimate,
- correlated noise,
- dead time,
- run-to-run variation.

Question:

```text
Which of these would dominate in a full SiPM characterization campaign?
```
