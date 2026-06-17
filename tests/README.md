# Automated Tests

Run the tests from the repository root after activating the virtual environment:

```bash
pytest
```

The starter version is expected to fail because `student/analysis.py` contains
TODO functions. As students complete those functions, the tests should begin to
pass.

The tests include two kinds of checks:

1. Small synthetic arrays with values that can be checked by hand.
2. Regression checks using `data/massibo_example.npy`.

The real-data checks are intentionally narrow. They verify that students used
the correct timing conversion, live-time definition, negative pulse amplitude
convention, and simple candidate-tagging rules.
