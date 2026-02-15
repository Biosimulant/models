# SPDX-FileCopyrightText: 2025-present Demi <bjaiye1@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Auto-generated tests for Wodarz1999CtlMemoryResponseHivBiomd0000000683Model.

These tests intentionally avoid requiring simulator dependencies. They should pass
even when a wrapper falls back to stub outputs (e.g., simulator not installed).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest


MODEL_ROOT = Path(__file__).resolve().parents[1]
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

def _find_repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "models" / "STANDARDS.md").exists():
            return p
    raise RuntimeError("repo root not found (models/STANDARDS.md missing)")

REPO_ROOT = _find_repo_root(Path(__file__).resolve())
BSIM_SRC = REPO_ROOT / "bsim" / "src"
if BSIM_SRC.exists() and str(BSIM_SRC) not in sys.path:
    # Ensure we import the real installable package at bsim/src/bsim/.
    sys.path.insert(0, str(BSIM_SRC))


from src.wodarz1999_ctl_memory_response_hiv_biomd0000000683_model import Wodarz1999CtlMemoryResponseHivBiomd0000000683Model  # noqa: E402
from bsim.signals import BioSignal  # noqa: E402


def test_instantiation() -> None:
    module = Wodarz1999CtlMemoryResponseHivBiomd0000000683Model()
    assert module.min_dt > 0
    assert isinstance(module.inputs(), set)
    assert isinstance(module.outputs(), set)
    assert len(module.outputs()) > 0


def test_advance_produces_outputs() -> None:
    module = Wodarz1999CtlMemoryResponseHivBiomd0000000683Model(min_dt=0.1)
    module.advance_to(0.1)
    outputs = module.get_outputs()
    for name in module.outputs():
        assert name in outputs
        signal = outputs[name]
        assert isinstance(signal, BioSignal)
        assert signal.source is not None
        assert signal.time == 0.1


def test_output_keys_match() -> None:
    module = Wodarz1999CtlMemoryResponseHivBiomd0000000683Model(min_dt=0.1)
    module.advance_to(0.1)
    assert set(module.get_outputs().keys()) == module.outputs()


def test_reset() -> None:
    module = Wodarz1999CtlMemoryResponseHivBiomd0000000683Model(min_dt=0.1)
    module.advance_to(0.1)
    if hasattr(module, "reset"):
        module.reset()
        module.advance_to(0.1)
        assert set(module.get_outputs().keys()) == module.outputs()
