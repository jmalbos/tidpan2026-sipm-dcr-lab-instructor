# Instructor Notes

## Suggested Timing

For a 90-minute session:

```text
0-10 min      MASSIBO and SiPM context
10-20 min     environment check and data model
20-40 min     loading, timing, live time, dark count rate
40-60 min     inter-arrival-time distribution
60-75 min     waveform amplitudes
75-85 min     crosstalk-like and afterpulse-like candidates
85-90 min     wrap-up discussion
```

For a 120-minute session, add:

```text
15 min        live peak-finding demonstration with scipy.signal.find_peaks
15 min        threshold scan or comparison with a second file
```

## Key Reference Values

For `data/massibo_example.npy`:

```text
events: 821
waveform samples per event: 251
live time: 458.375528 s
dark count rate: 1.791108 +/- 0.062510 Hz
raw DCR density: 49.753 +/- 1.736 mHz/mm^2
burst-tagged events: 289
burst-cleaned dark count rate: 1.160620 +/- 0.050319 Hz
burst-cleaned DCR density: 32.239 +/- 1.398 mHz/mm^2
burst-cleaned median amplitude: 13 ADC
crosstalk-like threshold: 32.5 ADC
burst-cleaned crosstalk-like candidates: 34
burst-cleaned afterpulse-like candidates, 1-100 us: 15
```

The inter-arrival-time distribution has a strong short-delay structure. This is
useful pedagogically: students should not conclude that the dataset is a perfect
Poisson process.

## Teaching Emphasis

- Real data are allowed to be imperfect; that is the point.
- The timestamp conversion is the most important technical convention.
- Live time must come from timestamps, not from the nominal 10-minute maximum.
- DCR should be quoted both as a total rate and normalized to the 36 mm^2 SiPM
  area.
- Burst tagging is separate from afterpulse tagging: DUNE-style burst tagging
  uses `dt_max = 100 ms` and `N_min = 5`.
- Pulse-amplitude and correlated-noise candidate counts should be evaluated on
  the burst-cleaned sample in this exercise.
- The amplitude convention follows the pulse polarity.
- Candidate tags are threshold-based approximations, not final physical truth.

## Recommended Live Demonstration

Show the MASSIBO setup first, then connect it to the file format:

```text
trigger timestamp -> column 0
digitized waveform -> columns 1:
clock/sample spacing -> 16 ns
```

If time allows, show one waveform and run `scipy.signal.find_peaks` on the
negative waveform. Keep this as a demonstration rather than a required task.

## Likely Help Points

- Students may have difficulty distinguishing event time from waveform time.
- Some will use the waveform sample axis to compute inter-arrival times.
- Some will assume crosstalk and afterpulse tags are mutually exclusive.
- Some will try to fit every feature instead of making the required simple
  estimates.

## Assessment Guidance

The automated tests check implementation mechanics. The final interpretation
questions should be reviewed qualitatively.

Look for:

- correct rate and uncertainty,
- recognition that the simple Poisson model is incomplete,
- sensible comments on short-delay excesses,
- awareness that thresholds affect candidate counts,
- caution about drawing broad conclusions from one file.
