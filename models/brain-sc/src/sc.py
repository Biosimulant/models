from __future__ import annotations

import bsim


class SC(bsim.BioModule):
    """Minimal example sink module consuming a vision signal."""

    def __init__(self):
        self.min_dt = 0.1

    def inputs(self):
        return {"vision"}

    def set_inputs(self, signals):
        if "vision" in signals:
            # Side effect is fine for local demos; platform UIs can ignore stdout.
            print("[SC] vision:", signals["vision"].value)

    def advance_to(self, t: float) -> None:
        return

    def get_outputs(self):
        return {}

