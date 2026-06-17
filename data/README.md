# MASSIBO Example Data

This directory contains one representative MASSIBO `.npy` file for the student
exercise.

Each row corresponds to one trigger from one SiPM sensor.

```text
column 0      timestamp in 62.5 MHz clock ticks
columns 1:    waveform ADC samples
```

Use:

```text
time_s = timestamp * 16e-9
```

The total acquisition time should be inferred from the first and last
timestamps, not assumed to be the nominal maximum of 10 minutes.

Larger optional datasets can be distributed separately through the instructor's
institutional cloud storage.
