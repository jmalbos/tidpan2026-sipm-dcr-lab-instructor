# Instructor Checklist

## One Week Before

- Confirm the public GitHub repository URL.
- Confirm that the school manual links to the lab repository.
- Upload optional larger MASSIBO datasets to institutional cloud storage.
- Decide whether solutions live in a private repo or remain local.
- Test setup on a clean machine or fresh virtual environment.

## Day Before

- Clone the student repository.
- Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

The starter repository should collect tests and fail because of TODO functions.

- Run the instructor solution in the private/instructor copy.
- Open the notebook and verify that the first waveform plot renders.
- Prepare backup screenshots or printed reference values.

## Start Of Session

- Show the MASSIBO setup or photos.
- Explain the difference between event timestamps and waveform sample time.
- State the timing convention: `1 tick = 16 ns`.
- State the area convention: `6 mm x 6 mm = 36 mm^2`.
- State the pulse convention: negative-going pulses.
- State the burst criterion: `dt_max = 100 ms`, `N_min = 5`.
- Point students to `student/analysis.py` and the notebook.

## During The Lab

- Encourage students to run `pytest` after every few functions.
- Watch for timestamp unit mistakes.
- Watch for positive-pulse amplitude calculations.
- Remind students that candidate tags are threshold-based approximations.
- Keep the final interpretation discussion even if some students do not finish
  every function.

## End Of Session

- Ask for the measured dark count rate.
- Ask for the burst-cleaned dark count rate in mHz/mm^2.
- Ask whether the process looks purely Poissonian.
- Discuss short-delay excesses and correlated noise.
- Connect threshold, overvoltage, and temperature to full SiPM
  characterization.
- Point fast students to `docs/extensions.md`.
