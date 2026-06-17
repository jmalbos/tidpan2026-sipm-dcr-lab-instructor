"""Export a clean public student repository from the instructor repository.

Usage
-----
From the instructor repository root:

    python tools/export_student_repo.py ../tidpan2026-sipm-dcr-lab

The destination directory is replaced, except for its `.git` directory if it
already exists.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PUBLIC_FILES = [
    ".gitignore",
    "README.md",
    "data",
    "docs/common_mistakes.md",
    "docs/extensions.md",
    "docs/lab_handout.md",
    "notebooks",
    "student",
    "tests",
]


PUBLIC_PYPROJECT = """[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "tidpan2026-sipm-dcr-lab"
version = "0.1.0"
description = "SiPM dark count rate laboratory exercise using MASSIBO data"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "numpy",
    "scipy",
    "matplotlib",
    "pandas",
    "jupyterlab",
    "ipykernel",
    "tqdm",
]

[project.optional-dependencies]
dev = [
    "pytest",
]

[tool.setuptools]
packages = []

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "destination",
        type=Path,
        help="Directory where the public student repository should be exported.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.cwd(),
        help="Instructor repository root. Defaults to the current directory.",
    )
    return parser.parse_args()


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                ".DS_Store",
                ".ipynb_checkpoints",
                ".pytest_cache",
                "*.pyc",
                "*.pyo",
                "*.egg-info",
            ),
        )
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def clear_destination(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for child in destination.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def export_student_repo(source_root: Path, destination_root: Path) -> None:
    source_root = source_root.resolve()
    destination_root = destination_root.resolve()

    if source_root == destination_root:
        raise ValueError("Destination must be different from the source repository.")
    if source_root in destination_root.parents:
        raise ValueError("Destination must not be inside the source repository.")

    clear_destination(destination_root)

    for relative in PUBLIC_FILES:
        source = source_root / relative
        destination = destination_root / relative
        if not source.exists():
            raise FileNotFoundError(f"Missing required public path: {source}")
        copy_path(source, destination)

    (destination_root / "pyproject.toml").write_text(PUBLIC_PYPROJECT, encoding="utf-8")


def main() -> None:
    args = parse_args()
    export_student_repo(args.source, args.destination)
    print(f"Exported public student repo to {args.destination.resolve()}")


if __name__ == "__main__":
    main()
