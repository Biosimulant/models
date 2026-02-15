#!/usr/bin/env python3
"""
Virtual Cell drug-to-neural-effect demo.

Demonstrates a multi-scale simulation pipeline:
- PerturbationSource emits an SCN1A gene knockout at t=0.1s
- VirtualCell (GRN model) predicts transcriptional response
- ExpressionTranslator maps gene expression changes to biophysical current
- IzhikevichPopulation fires in response to the translated current
- Monitors collect spike rasters, firing rates, and metrics

The simulation shows how a molecular-level perturbation (gene knockout)
cascades through gene regulatory networks to alter neural circuit activity,
inspired by the Arc Institute's Virtual Cell concept.

Run:
    pip install "bsim @ git+https://github.com/BioSimulant/bsim.git@<ref>"
    python spaces/virtualcell-drug-neural-effect/run_local.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import bsim

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
for _model in [
    "virtualcell-perturbation-source",
    "virtualcell-arc-grn",
    "virtualcell-expression-translator",
    "virtualcell-expression-monitor",
    "neuro-izhikevich-population",
    "neuro-spike-monitor",
    "neuro-rate-monitor",
    "neuro-spike-metrics",
]:
    sys.path.insert(0, str(MODELS_DIR / _model))

from src.perturbation_source import PerturbationSource
from src.virtual_cell import VirtualCell
from src.expression_translator import ExpressionTranslator
from src.expression_monitor import ExpressionMonitor
from src.izhikevich import IzhikevichPopulation
from src.spike_monitor import SpikeMonitor
from src.rate_monitor import RateMonitor
from src.neuro_metrics import NeuroMetrics


def run_knockout_demo(gene: str = "SCN1A", base_current: float = 8.0) -> dict:
    """Run a gene knockout simulation and observe neural effects.

    Args:
        gene: Gene to knock out.
        base_current: Baseline injected current before perturbation.

    Returns:
        Dict with simulation results and collected visuals.
    """
    print(f"\n{'=' * 60}")
    print(f"VirtualCell Demo: {gene} Knockout")
    print(f"Base current: {base_current} uA/cm^2")
    print("=" * 60)

    world = bsim.BioWorld()

    # Molecular-level modules
    pert_source = PerturbationSource(
        gene=gene, pert_type="knockout", magnitude=0.0, apply_at=0.1,
    )
    cell = VirtualCell(n_genes=20, decay_rate=0.3, response_speed=5.0, seed=42)
    translator = ExpressionTranslator(base_current=base_current)
    expr_monitor = ExpressionMonitor(max_points=5000)

    # Circuit-level modules
    neurons = IzhikevichPopulation(n=20, preset="RS", sample_indices=[0, 1, 2])
    spike_mon = SpikeMonitor(max_neurons=20, width=600, height=200)
    rate_mon = RateMonitor(window_size=0.02, n_neurons=20)
    metrics = NeuroMetrics(n_neurons=20)

    # Wire modules
    wb = bsim.WiringBuilder(world)
    wb.add("perturbation", pert_source)
    wb.add("virtual_cell", cell)
    wb.add("translator", translator)
    wb.add("expr_mon", expr_monitor)
    wb.add("neuron", neurons)
    wb.add("spike_mon", spike_mon)
    wb.add("rate_mon", rate_mon)
    wb.add("metrics", metrics)

    # Perturbation -> VirtualCell -> Translator -> Neurons -> Monitors
    wb.connect("perturbation.perturbation", ["virtual_cell.perturbation"])
    wb.connect("virtual_cell.expression_profile", ["translator.expression_profile", "expr_mon.expression_profile"])
    wb.connect("translator.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["spike_mon.spikes", "rate_mon.spikes", "metrics.spikes"])
    wb.apply()

    # Run for 1 second at 1ms ticks
    world.run(duration=1.0, tick_dt=0.001)

    # Collect and display results
    visuals = world.collect_visuals()
    print(f"\nCollected {len(visuals)} visual outputs:")
    for entry in visuals:
        vis_types = [v["render"] for v in entry["visuals"]] if isinstance(entry["visuals"], list) else [entry["visuals"]["render"]]
        print(f"  - {entry['module']}: {vis_types}")

    # Print metrics
    for entry in visuals:
        if entry["module"] == "NeuroMetrics":
            table = entry["visuals"]
            if isinstance(table, list):
                table = table[0]
            print("\nNeural Metrics:")
            for row in table["data"]["rows"]:
                print(f"  {row[0]}: {row[1]}")

    # Print expression summary
    expr_out = world.get_outputs("virtual_cell")
    if "expression_summary" in expr_out:
        summary = expr_out["expression_summary"].value
        print("\nExpression Summary:")
        print(f"  Mean fold-change: {summary['mean_fold_change']:.3f}")
        if summary["top_down"]:
            print("  Top downregulated:")
            for g in summary["top_down"]:
                print(f"    {g['gene']}: {g['fold_change']:.3f}x")
        if summary["top_up"]:
            print("  Top upregulated:")
            for g in summary["top_up"]:
                print(f"    {g['gene']}: {g['fold_change']:.3f}x")

    # Print translated current
    translator_out = world.get_outputs("translator")
    if "current" in translator_out:
        current = translator_out["current"].value
        print(f"\n  Translated current: {current:.2f} uA/cm^2 (base: {base_current})")

    return {"visuals": visuals}


def main() -> None:
    """Run demos with different gene knockouts."""
    print("VirtualCell: Drug Effect on Neural Circuit")
    print("=" * 60)
    print("Demonstrating multi-scale simulation:")
    print("  Gene perturbation -> GRN dynamics -> Biophysical current -> Spiking neurons")
    print()

    # Demo 1: SCN1A knockout (sodium channel — reduces excitability)
    run_knockout_demo("SCN1A", base_current=8.0)

    # Demo 2: KCNA1 knockout (potassium channel — increases excitability)
    run_knockout_demo("KCNA1", base_current=8.0)

    # Demo 3: BDNF knockout (neurotrophic factor — broad downstream effects)
    run_knockout_demo("BDNF", base_current=8.0)

    # Demo 4: Compare baseline vs perturbed
    print(f"\n{'=' * 60}")
    print("Comparison: SCN1A knockout effect on spike count")
    print("=" * 60)

    for gene in ["SCN1A", "KCNA1", "GAD1", "GRIA1", "BDNF"]:
        world = bsim.BioWorld()
        pert = PerturbationSource(gene=gene, pert_type="knockout", magnitude=0.0, apply_at=0.1)
        cell = VirtualCell(n_genes=20, seed=42)
        translator = ExpressionTranslator(base_current=8.0)
        neurons = IzhikevichPopulation(n=20, preset="RS")
        metrics = NeuroMetrics(n_neurons=20)

        wb = bsim.WiringBuilder(world)
        wb.add("pert", pert)
        wb.add("cell", cell)
        wb.add("trans", translator)
        wb.add("neuron", neurons)
        wb.add("metrics", metrics)
        wb.connect("pert.perturbation", ["cell.perturbation"])
        wb.connect("cell.expression_profile", ["trans.expression_profile"])
        wb.connect("trans.current", ["neuron.current"])
        wb.connect("neuron.spikes", ["metrics.spikes"])
        wb.apply()

        world.run(duration=0.5, tick_dt=0.001)

        met_out = world.get_outputs("metrics")
        trans_out = world.get_outputs("trans")
        current = trans_out["current"].value if "current" in trans_out else 0.0
        vis = metrics.visualize()
        if vis:
            table = vis if isinstance(vis, dict) else vis[0]
            spikes = table["data"]["rows"][0][1]
            print(f"  {gene:8s} knockout -> current={current:6.2f} uA/cm^2, spikes={spikes}")


if __name__ == "__main__":
    main()
