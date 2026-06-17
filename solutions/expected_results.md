# Expected Results

These values are generated from `data/massibo_example.npy` using
`solutions/instructor_solution.py`.

## Dataset Checks

| Quantity | Value |
| --- | ---: |
| events | 821 |
| waveform samples per event | 251 |
| live time | 458.375528 s |

## Dark Count Rate

| Quantity | Value |
| --- | ---: |
| dark count rate | 1.791108 Hz |
| Poisson standard uncertainty | 0.062510 Hz |
| dark count rate density | 49.753 mHz/mm^2 |
| density standard uncertainty | 1.736 mHz/mm^2 |

The rate is computed as:

```text
rate = n_events / (last_time - first_time)
sigma_rate = sqrt(n_events) / (last_time - first_time)
```

The acquisition duration is inferred from timestamps, not assumed to be the
nominal maximum of 10 minutes.

The SiPM active area is treated as:

```text
6 mm x 6 mm = 36 mm^2
```

## Burst Removal

Burst candidates are tagged using:

```text
dt_max = 100 ms
n_min = 5 consecutive events
```

| Quantity | Value |
| --- | ---: |
| burst-tagged events | 289 |
| non-burst events | 532 |
| burst-cleaned dark count rate | 1.160620 Hz |
| burst-cleaned rate uncertainty | 0.050319 Hz |
| burst-cleaned DCR density | 32.239 mHz/mm^2 |
| burst-cleaned density uncertainty | 1.398 mHz/mm^2 |

## Inter-Arrival Times

| Quantity | Value |
| --- | ---: |
| mean inter-arrival time | 0.558995 s |
| exponential MLE rate | 1.788926 Hz |
| KS diagnostic D | 0.323945 |
| KS diagnostic p-value | 4.30676e-77 |

The KS value is a classroom diagnostic because the exponential scale is
estimated from the same data. The very small p-value is still useful as a
discussion point: the sample contains short-delay correlated events, so the
simple Poisson model is incomplete.

## Burst-Cleaned Waveform Features

| Quantity | Value |
| --- | ---: |
| median negative pulse amplitude | 13.000 ADC |
| 95th percentile amplitude | 38.000 ADC |
| 99th percentile amplitude | 171.690 ADC |
| median pulse sample index | 63.0 |

## Rule-Based Candidate Tags

Default instructor thresholds:

```text
crosstalk-like threshold = 2.5 * median amplitude = 32.500 ADC
afterpulse-like delay window = 1 us to 100 us
prompt short-delay window = 0 us to 10 us
isolated-event minimum previous delay = 1 ms
```

| Candidate class | Count |
| --- | ---: |
| burst-cleaned crosstalk-like high-amplitude candidates | 34 |
| burst-cleaned afterpulse-like candidates, 1-100 us | 15 |
| burst-cleaned prompt short-delay candidates, <=10 us | 12 |
| burst-cleaned isolated dark-count-like events | 477 |
