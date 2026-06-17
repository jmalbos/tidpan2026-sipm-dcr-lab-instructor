# Distribution Checklist

Use this checklist when preparing the GitHub repositories for the school.

## Recommended Repositories

```text
TIDPAN2026                         existing school/manual repository
tidpan2026-sipm-dcr-lab            public student lab repository
tidpan2026-sipm-dcr-lab-instructor private instructor repository or local copy
```

The existing `TIDPAN2026` repository should link to the public student lab
repository.

## Public Student Repository

Include:

```text
README.md
pyproject.toml
.gitignore

data/
  massibo_example.npy
  README.md

notebooks/
  01_sipm_dark_counts.ipynb

student/
  analysis.py
  README.md

tests/
  conftest.py
  test_classification.py
  test_io.py
  test_statistics.py
  test_timing.py
  test_waveforms.py
  README.md

docs/
  lab_handout.md
  common_mistakes.md
  extensions.md
```

For the public repository, `pyproject.toml` should not point to `src/` because
the reference helper package is instructor-only. Use:

```toml
[tool.setuptools]
packages = []

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

Do not include:

```text
solutions/
docs/instructor_notes.md
docs/instructor_checklist.md
docs/live_demo_script.md
docs/distribution.md
src/
.venv/
.pytest_cache/
__pycache__/
*.egg-info/
.DS_Store
```

## Private Instructor Repository

Include everything in the public student repository plus:

```text
src/
  sipm_lab/

solutions/
docs/instructor_notes.md
docs/instructor_checklist.md
docs/live_demo_script.md
docs/distribution.md
```

## Before Publishing

- Confirm permission to publish `data/massibo_example.npy`.
- Confirm that the public repository does not contain `solutions/`.
- Confirm that instructor-only docs are absent from the public repository.
- Confirm that the notebook opens from a fresh clone.
- Confirm that the starter tests collect:

```bash
pytest --collect-only -q
```

- Confirm that the starter tests fail only because of `NotImplementedError`.

## Suggested Public Release Commands

From the instructor repository, export the public student repository:

```bash
python tools/export_student_repo.py ../tidpan2026-sipm-dcr-lab
```

Then, from the clean student-copy directory:

```bash
git init
git add .
git commit -m "Add SiPM dark count rate lab"
git branch -M main
git remote add origin git@github.com:<your-org>/tidpan2026-sipm-dcr-lab.git
git push -u origin main
```

## GitHub Actions

Do not add a normal CI workflow that runs `pytest` on the starter repository,
because the public starter code is expected to fail until students complete the
TODO functions.

If CI is desired, use one of these approaches:

- run only `pytest --collect-only`,
- run tests against an instructor solution branch,
- add a separate smoke test for package installation and notebook JSON validity.

## Student Instructions To Link From TIDPAN2026

Suggested text:

```text
SiPM dark count rate laboratory:
https://github.com/<your-org>/tidpan2026-sipm-dcr-lab

Before the session, clone the repository and follow the setup instructions in
the README.
```
