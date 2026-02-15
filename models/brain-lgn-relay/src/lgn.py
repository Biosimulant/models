from __future__ import annotations

import bsim


class LGN(bsim.BioModule):
    """Minimal example relay module: retina -> thalamus."""

    def __init__(self):
        self.min_dt = 0.1
        self._outputs = {}

    def inputs(self):
        return {"retina"}

    def outputs(self):
        return {"thalamus"}

    def set_inputs(self, signals):
        if "retina" in signals:
            sig = signals["retina"]
            self._outputs = {
                "thalamus": bsim.BioSignal(source="lgn", name="thalamus", value=sig.value, time=sig.time)
            }

    def advance_to(self, t: float) -> None:
        return

    def get_outputs(self):
        return dict(self._outputs)

