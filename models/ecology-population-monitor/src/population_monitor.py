# SPDX-FileCopyrightText: 2025-present Demi <bjaiye1@gmail.com>
#
# SPDX-License-Identifier: MIT
"""Population monitor: collect and visualize population data from multiple species."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - typing only
    from bsim import BioWorld
    from bsim.visuals import VisualSpec

from bsim import BioModule
from bsim.signals import BioSignal


class PopulationMonitor(BioModule):
    """Collects population data from multiple species and visualizes them together.

    Receives `population_state` signals and produces a combined timeseries plot.

    Parameters:
        max_points: Maximum data points per species (oldest dropped).
    """

    def __init__(self, max_points: int = 10000, min_dt: float = 1.0) -> None:
        self.min_dt = min_dt
        self.max_points = max_points
        self._data: Dict[str, List[Dict[str, float]]] = {}

    def inputs(self) -> Set[str]:
        return {"population_state"}

    def outputs(self) -> Set[str]:
        return set()

    def reset(self) -> None:
        """Reset collected data."""
        self._data = {}

    def set_inputs(self, signals: Dict[str, BioSignal]) -> None:
        signal = signals.get("population_state")
        if signal is None or not isinstance(signal.value, dict):
            return
        species = str(signal.value.get("species", "Unknown"))
        count = int(signal.value.get("count", 0))
        t = float(signal.value.get("t", signal.time))

        if species not in self._data:
            self._data[species] = []

        self._data[species].append({"t": t, "count": count})

        # Trim if over limit
        if len(self._data[species]) > self.max_points:
            self._data[species] = self._data[species][-self.max_points:]

    def advance_to(self, t: float) -> None:
        return

    def get_outputs(self) -> Dict[str, BioSignal]:
        return {}

    def visualize(self) -> Optional["VisualSpec"]:
        """Generate combined population timeseries for all species."""
        if not self._data:
            return None

        series = []
        for species in sorted(self._data.keys()):
            history = self._data[species]
            series.append({
                "name": species,
                "points": [[h["t"], h["count"]] for h in history],
            })

        return {
            "render": "timeseries",
            "data": {
                "series": series,
                "title": "Population Dynamics",
            },
        }
