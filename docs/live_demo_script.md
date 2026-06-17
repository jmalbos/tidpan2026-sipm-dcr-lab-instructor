# Live Demonstration Script

## Goal

Connect the physical MASSIBO setup to the data structure students will analyze:

```text
SiPM signal -> trigger -> timestamp + digitized waveform
```

Recommended duration:

```text
90-minute lab: 10-15 minutes
120-minute lab: 20-25 minutes
```

## Before Students Arrive

- Check that the example notebook opens.
- Check that `data/massibo_example.npy` is present.
- Have one waveform plot ready in case live plotting is slow.
- If showing hardware, decide which components students can safely approach.
- Prepare one sentence on how MASSIBO is used for DUNE-related SiPM
  characterization.

## Demo Flow

### 1. Physical Setup

Show:

- SiPM or SiPM carrier, if visible,
- cryogenic environment or liquid-nitrogen connection,
- readout/electronics chain,
- trigger/acquisition computer.

Say:

```text
In this lab, we are not analyzing simulated detector output. Each row in the
file corresponds to a real trigger recorded by MASSIBO for one SiPM sensor.
```

Ask:

```text
What can produce a trigger if no light source is intentionally pulsed?
```

Expected ideas:

- thermal generation,
- tunneling or field-assisted carriers,
- correlated noise,
- electronics noise or threshold effects.

### 2. From Trigger To File Row

Show the data model:

```text
column 0      timestamp in 62.5 MHz clock ticks
columns 1:    ADC waveform samples
```

Say:

```text
The first column tells us when the trigger happened. The remaining columns show
the waveform around that trigger.
```

Emphasize:

```text
event time and waveform time are different axes.
```

### 3. Timing Convention

Write or show:

```text
62.5 MHz clock -> 16 ns per tick
time_s = timestamp * 16e-9
```

Ask:

```text
Why should we infer live time from timestamps instead of assuming 10 minutes?
```

Expected answer:

- acquisition can stop early,
- trigger limits can be reached,
- real runs are not always exactly nominal duration.

### 4. Waveform Preview

Open the notebook and run the first waveform plot, or show a prepared plot.

Point out:

- baseline near a stable ADC level,
- negative-going pulse,
- pulse occurring after pre-trigger samples,
- waveform duration of about 4 us.

Say:

```text
For this lab we will use a simple amplitude definition:
baseline minus the minimum ADC value.
```

### 5. Optional Peak-Finding Demonstration

If time allows:

```python
from scipy.signal import find_peaks

waveform = waveforms[0]
peaks, properties = find_peaks(-waveform, prominence=5)
```

Keep this short. The required lab does not depend on detailed peak finding.

Ask:

```text
What might go wrong if we simply search for the largest sample in every
waveform?
```

Expected ideas:

- wrong polarity,
- noise fluctuations,
- baseline shifts,
- multiple pulses,
- saturated or unusual events.

### 6. Hand Off To Students

Say:

```text
Your task is to turn these triggers into a dark count rate, identify burst-like
sequences, remove their contribution, and then check whether the remaining
event times behave like a simple Poisson process.
```

Point students to:

```text
student/analysis.py
notebooks/01_sipm_dark_counts.ipynb
pytest
```

## Backup Path

If Jupyter or plotting fails:

1. Use the instructor solution summary values.
2. Sketch the waveform convention on the board.
3. Have students work through the timing and rate calculation with the provided
   reference values.
4. Resume coding once the environment issue is resolved.

Reference values:

```text
events: 821
live time: 458.375528 s
dark count rate: 1.791108 +/- 0.062510 Hz
raw DCR density: 49.753 +/- 1.736 mHz/mm^2
burst-tagged events: 289
burst-cleaned DCR: 1.160620 +/- 0.050319 Hz
burst-cleaned DCR density: 32.239 +/- 1.398 mHz/mm^2
burst-cleaned median amplitude: 13 ADC
burst-cleaned crosstalk-like candidates: 34
burst-cleaned afterpulse-like candidates, 1-100 us: 15
```

## Discussion Prompts

- Why does cooling reduce the dark count rate?
- Why can a single primary avalanche produce a larger-than-usual pulse?
- Why are very short inter-arrival times suspicious in a Poisson model?
- How is a burst different from a single afterpulse candidate?
- How would the analysis change if several SiPMs were compared?
- Which quantities would need metadata in a full characterization campaign?
