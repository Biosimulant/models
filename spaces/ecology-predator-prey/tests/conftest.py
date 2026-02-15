from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SPACE_DIR = Path(__file__).resolve().parents[1]
_MODELS_DIR = _SPACE_DIR.parent.parent / "models"

_DEPS = [
    "ecology-abiotic-environment",
    "ecology-organism-population",
    "ecology-predator-prey-interaction",
    "ecology-population-monitor",
    "ecology-phase-space-monitor",
    "ecology-population-metrics",
]


@pytest.fixture(scope="session", autouse=True)
def _paths():
    for d in _DEPS:
        p = str(_MODELS_DIR / d)
        if p not in sys.path:
            sys.path.insert(0, p)


@pytest.fixture(scope="session")
def bsim(_paths):
    import bsim as _bsim

    return _bsim

