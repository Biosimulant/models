#!/usr/bin/env python3
"""
Hodgkin-Huxley neuron demo.

Demonstrates:
- The classic 1952 squid giant axon conductance-based model
- Subthreshold, near-threshold, and spiking regimes
- Frequency-current (f-I) relationship
- Detailed gating variable and ionic current monitoring

Run:
    pip install "bsim @ git+https://github.com/BioSimulant/bsim.git@<ref>"
    python spaces/neuro-hh-neuron/run_local.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import bsim

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
for _model in [
    "neuro-step-current",
    "neuro-hh-population",
    "neuro-spike-monitor",
    "neuro-state-monitor",
    "neuro-hh-state-monitor",
    "neuro-metrics",
]:
    sys.path.insert(0, str(MODELS_DIR / _model))

from src.step_current import StepCurrent
from src.hodgkin_huxley import HodgkinHuxleyPopulation
from src.spike_monitor import SpikeMonitor
from src.state_monitor import StateMonitor
from src.hh_state_monitor import HHStateMonitor
from src.neuro_metrics import NeuroMetrics


def run_hh_neuron(I_current: float = 10.0, duration: float = 0.1) -> dict:
    """Run a single HH neuron with given current injection.

    Args:
        I_current: Injected current amplitude (uA/cm^2).
        duration: Simulation duration in seconds.

    Returns:
        Dict with simulation result and collected visuals.
    """
    print(f"\n{'=' * 60}")
    print(f"Running HH neuron with I = {I_current} uA/cm^2, duration = {duration*1000:.0f}ms")
    print("=" * 60)

    world = bsim.BioWorld()

    # Create modules
    current_source = StepCurrent(I=I_current)
    neuron = HodgkinHuxleyPopulation(n=1, sample_indices=[0])
    spike_monitor = SpikeMonitor(max_neurons=1, width=600, height=200)
    state_monitor = StateMonitor(max_points=10000)
    hh_monitor = HHStateMonitor(max_points=10000, neuron_index=0)
    metrics = NeuroMetrics(n_neurons=1)

    # Wire modules
    wb = bsim.WiringBuilder(world)
    wb.add("current", current_source)
    wb.add("neuron", neuron)
    wb.add("spike_mon", spike_monitor)
    wb.add("state_mon", state_monitor)
    wb.add("hh_mon", hh_monitor)
    wb.add("metrics", metrics)

    wb.connect("current.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["spike_mon.spikes", "metrics.spikes"])
    wb.connect("neuron.state", ["state_mon.state", "hh_mon.state"])
    wb.apply()

    # Simulate with fine time step (0.05ms = 50us)
    world.run(duration=duration, tick_dt=0.00005)

    # Collect visuals
    visuals = world.collect_visuals()
    print(f"\nCollected {len(visuals)} visual outputs:")
    for entry in visuals:
        vis_list = entry["visuals"]
        if isinstance(vis_list, list):
            print(f"  - {entry['module']}: {[v['render'] for v in vis_list]}")
        elif vis_list is not None:
            print(f"  - {entry['module']}: {vis_list['render']}")

    # Print metrics
    for entry in visuals:
        if entry["module"] == "NeuroMetrics":
            vis = entry["visuals"]
            if vis is not None:
                table_data = vis["data"]
                print("\nMetrics:")
                for row in table_data["rows"]:
                    print(f"  {row[0]}: {row[1]}")

    return {"visuals": visuals}


def run_fi_curve() -> None:
    """Sweep current amplitudes to generate a frequency-current (f-I) curve."""
    print("\n" + "=" * 60)
    print("Frequency-Current (f-I) Curve")
    print("=" * 60)

    currents = [0, 2, 4, 5, 6, 7, 8, 10, 15, 20, 30, 50]
    duration = 0.5  # 500ms per trial

    print(f"\n{'I (uA/cm^2)':>15} | {'Spikes':>8} | {'Rate (Hz)':>10}")
    print("-" * 40)

    for I in currents:
        world = bsim.BioWorld()

        current_source = StepCurrent(I=float(I))
        neuron = HodgkinHuxleyPopulation(n=1, sample_indices=[0])
        metrics = NeuroMetrics(n_neurons=1)

        wb = bsim.WiringBuilder(world)
        wb.add("current", current_source)
        wb.add("neuron", neuron)
        wb.add("metrics", metrics)

        wb.connect("current.current", ["neuron.current"])
        wb.connect("neuron.spikes", ["metrics.spikes"])
        wb.apply()

        world.run(duration=duration, tick_dt=0.00005)

        # Extract spike count
        visuals = world.collect_visuals()
        spike_count = 0
        for entry in visuals:
            if entry["module"] == "NeuroMetrics":
                vis = entry["visuals"]
                if vis is not None:
                    rows = vis["data"]["rows"]
                    spike_count = int(rows[0][1])  # "Total Spikes"

        rate = spike_count / duration
        print(f"{I:>15} | {spike_count:>8} | {rate:>10.1f}")


def main() -> None:
    """Run HH neuron demos at different current levels."""
    print("Hodgkin-Huxley Neuron Demo")
    print("=" * 60)
    print("Model: Hodgkin & Huxley (1952) squid giant axon")
    print("Parameters: g_Na=120, g_K=36, g_L=0.3 mS/cm^2")
    print("            E_Na=50, E_K=-77, E_L=-54.387 mV")

    # Demo 1: Subthreshold (no spikes)
    run_hh_neuron(I_current=5.0, duration=0.05)

    # Demo 2: Near threshold
    run_hh_neuron(I_current=7.0, duration=0.1)

    # Demo 3: Spiking regime
    run_hh_neuron(I_current=10.0, duration=0.1)

    # Demo 4: Fast spiking
    run_hh_neuron(I_current=20.0, duration=0.1)

    # Demo 5: f-I curve
    run_fi_curve()


if __name__ == "__main__":
    main()
