# TIDPAN 2026 SiPM Dark Count Rate Lab

Graduate-level laboratory exercise for characterizing random noise in silicon
photomultipliers operated at liquid-nitrogen temperature, using real MASSIBO
data.

## Student Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Optional, but recommended for a named notebook kernel:

```bash
python -m ipykernel install --user --name sipm-dcr-lab --display-name "SiPM DCR Lab"
```

Start the notebook interface:

```bash
jupyter lab
```

Open:

```text
notebooks/01_sipm_dark_counts.ipynb
```

Students should complete the TODOs in:

```text
student/analysis.py
```

Run the automated checks with:

```bash
pytest
```

The starter version fails these tests until the TODO functions are completed.

## Repository Layout

```text
data/          example MASSIBO data file and dataset notes
notebooks/     student-facing interactive notebook
student/       functions completed by students
tests/         automated checks for student work
docs/          handout, common mistakes, and extensions
```

## Data Model

The example data are stored as a NumPy `.npy` array. Each row is one MASSIBO
trigger for one SiPM sensor.

```text
column 0      event timestamp in 62.5 MHz clock ticks
columns 1:    ADC waveform samples
```

Timing convention:

```text
1 tick = 16 ns
1 waveform sample = 16 ns
251 waveform samples = approximately 4.016 us
```

The waveforms in the teaching example are negative-going pulses.
