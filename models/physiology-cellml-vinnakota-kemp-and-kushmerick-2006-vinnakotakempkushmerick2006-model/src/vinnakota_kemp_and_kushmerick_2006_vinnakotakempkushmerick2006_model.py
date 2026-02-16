# SPDX-FileCopyrightText: 2025-present Demi <bjaiye1@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Auto-generated CellML BioModule wrapper for Vinnakota, Kemp and Kushmerick, 2006.

Source: physiome:vinnakota_kemp_kushmerick_2006
Original: https://models.physiomeproject.org/workspace/vinnakota_kemp_kushmerick_2006
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - typing only
    from bsim import BioWorld

import bsim
from bsim.signals import BioSignal, SignalMetadata


class CellmlVinnakotaKempAndKushmerick2006(bsim.BioModule):
    """BioModule wrapper for CellML model: Vinnakota, Kemp and Kushmerick, 2006."""

    def __init__(self, model_path: str = "data/vinnakota_kemp_kushmeric_2006_exp29frA02.cellml", min_dt: float = 0.01) -> None:
        self.min_dt = min_dt
        self._model_path = Path(__file__).parent.parent / model_path
        self._t = 0.0
        self._model = None
        self._stub: bool = False
        self._outputs: Dict[str, BioSignal] = {}

    @staticmethod
    def _is_placeholder_file(path: Path) -> bool:
        try:
            head = path.open("rb").read(160)
        except OSError:
            return True
        try:
            text = head.decode("utf-8", errors="ignore")
        except Exception:
            return False
        return "Placeholder:" in text

    def setup(self, config: Optional[Dict[str, Any]] = None) -> None:
        if self._is_placeholder_file(self._model_path):
            self._stub = True
            self._model = None
            self._t = 0.0
            return

        try:
            import libcellml
        except Exception:
            self._stub = True
            self._model = None
            self._t = 0.0
            return

        parser = libcellml.Parser()
        self._model = parser.parseModel(self._model_path.read_text(encoding="utf-8"))
        self._t = 0.0

    def reset(self) -> None:
        self._t = 0.0
        self._outputs = {}

    def inputs(self) -> Set[str]:
        return set()

    def outputs(self) -> Set[str]:
        return {"state"}

    def advance_to(self, t: float) -> None:
        if self._model is None and not self._stub:
            self.setup()
        self._t = t
        source_name = getattr(self, "_world_name", self.__class__.__name__)
        self._outputs = {
            "state": BioSignal(
                source=source_name,
                name="state",
                value={"t": t, "placeholder": self._stub},
                time=t,
                metadata=SignalMetadata(
                    description="CellML model state",
                    kind="state",
                ),
            )
        }

    def get_outputs(self) -> Dict[str, BioSignal]:
        return dict(self._outputs)

# Canonical alias for stable entrypoint naming.
VinnakotaKempAndKushmerick2006Vinnakotakempkushmerick2006Model = CellmlVinnakotaKempAndKushmerick2006
