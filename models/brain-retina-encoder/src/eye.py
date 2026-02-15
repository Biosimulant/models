from __future__ import annotations

import bsim


class Eye(bsim.BioModule):
    """Minimal example module producing a time-varying visual stream."""

    def __init__(self):
        self.min_dt = 0.1
        self._outputs = {}

    def outputs(self):
        return {"visual_stream"}

    def advance_to(self, t: float) -> None:
        self._outputs = {
            "visual_stream": bsim.BioSignal(source="eye", name="visual_stream", value=t, time=t)
        }

    def get_outputs(self):
        return dict(self._outputs)

