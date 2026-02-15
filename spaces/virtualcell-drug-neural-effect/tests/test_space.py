"""Integration tests for the virtualcell-drug-neural-effect space."""
from __future__ import annotations


def test_space_loads(bsim):
    """All models instantiate and wire without errors."""
    from src.perturbation_source import PerturbationSource
    from src.virtual_cell import VirtualCell
    from src.expression_translator import ExpressionTranslator
    from src.expression_monitor import ExpressionMonitor
    from src.izhikevich import IzhikevichPopulation
    from src.spike_monitor import SpikeMonitor
    from src.rate_monitor import RateMonitor
    from src.neuro_metrics import NeuroMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("perturbation", PerturbationSource(gene="SCN1A", pert_type="knockout", magnitude=0.0, apply_at=0.1))
    wb.add("virtual_cell", VirtualCell(n_genes=20, seed=42))
    wb.add("translator", ExpressionTranslator(base_current=8.0))
    wb.add("expr_mon", ExpressionMonitor(max_points=5000))
    wb.add("neuron", IzhikevichPopulation(n=20, preset="RS", sample_indices=[0, 1, 2]))
    wb.add("spike_mon", SpikeMonitor(max_neurons=20, width=600, height=200))
    wb.add("rate_mon", RateMonitor(window_size=0.02, n_neurons=20))
    wb.add("metrics", NeuroMetrics(n_neurons=20))

    wb.connect("perturbation.perturbation", ["virtual_cell.perturbation"])
    wb.connect("virtual_cell.expression_profile", ["translator.expression_profile", "expr_mon.expression_profile"])
    wb.connect("translator.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["spike_mon.spikes", "rate_mon.spikes", "metrics.spikes"])
    wb.apply()

    assert len(world.module_names) == 8


def test_simulation_runs(bsim):
    """Simulation completes without crashing."""
    from src.perturbation_source import PerturbationSource
    from src.virtual_cell import VirtualCell
    from src.expression_translator import ExpressionTranslator
    from src.expression_monitor import ExpressionMonitor
    from src.izhikevich import IzhikevichPopulation
    from src.spike_monitor import SpikeMonitor
    from src.rate_monitor import RateMonitor
    from src.neuro_metrics import NeuroMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("perturbation", PerturbationSource(gene="SCN1A", pert_type="knockout", magnitude=0.0, apply_at=0.05))
    wb.add("virtual_cell", VirtualCell(n_genes=20, seed=42))
    wb.add("translator", ExpressionTranslator(base_current=8.0))
    wb.add("expr_mon", ExpressionMonitor())
    wb.add("neuron", IzhikevichPopulation(n=5, preset="RS"))
    wb.add("spike_mon", SpikeMonitor(max_neurons=5))
    wb.add("rate_mon", RateMonitor(n_neurons=5))
    wb.add("metrics", NeuroMetrics(n_neurons=5))

    wb.connect("perturbation.perturbation", ["virtual_cell.perturbation"])
    wb.connect("virtual_cell.expression_profile", ["translator.expression_profile", "expr_mon.expression_profile"])
    wb.connect("translator.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["spike_mon.spikes", "rate_mon.spikes", "metrics.spikes"])
    wb.apply()

    # Run a short simulation (0.2s at 1ms ticks)
    world.run(duration=0.2, tick_dt=0.001)


def test_signals_flow(bsim):
    """Outputs propagate through the wiring graph."""
    from src.perturbation_source import PerturbationSource
    from src.virtual_cell import VirtualCell
    from src.expression_translator import ExpressionTranslator
    from src.izhikevich import IzhikevichPopulation
    from src.neuro_metrics import NeuroMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("perturbation", PerturbationSource(gene="SCN1A", pert_type="knockout", magnitude=0.0, apply_at=0.0))
    wb.add("virtual_cell", VirtualCell(n_genes=20, seed=42))
    wb.add("translator", ExpressionTranslator(base_current=8.0))
    wb.add("neuron", IzhikevichPopulation(n=5, preset="RS"))
    wb.add("metrics", NeuroMetrics(n_neurons=5))

    wb.connect("perturbation.perturbation", ["virtual_cell.perturbation"])
    wb.connect("virtual_cell.expression_profile", ["translator.expression_profile"])
    wb.connect("translator.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["metrics.spikes"])
    wb.apply()

    world.run(duration=0.3, tick_dt=0.001)

    # Verify each stage produced outputs
    pert_out = world.get_outputs("perturbation")
    assert "perturbation" in pert_out
    assert pert_out["perturbation"].value["active"] is True

    vc_out = world.get_outputs("virtual_cell")
    assert "expression_profile" in vc_out
    profile = vc_out["expression_profile"].value
    assert len(profile["gene_names"]) == 20

    trans_out = world.get_outputs("translator")
    assert "current" in trans_out
    current = trans_out["current"].value
    assert isinstance(current, float)

    # SCN1A knockout should reduce excitatory current below base
    assert current < 8.0, f"Expected current < 8.0 after SCN1A KO, got {current}"


def test_visuals_collected(bsim):
    """Visualization specs are returned after simulation."""
    from src.perturbation_source import PerturbationSource
    from src.virtual_cell import VirtualCell
    from src.expression_translator import ExpressionTranslator
    from src.expression_monitor import ExpressionMonitor
    from src.izhikevich import IzhikevichPopulation
    from src.spike_monitor import SpikeMonitor
    from src.rate_monitor import RateMonitor
    from src.neuro_metrics import NeuroMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("perturbation", PerturbationSource(gene="SCN1A", pert_type="knockout", magnitude=0.0, apply_at=0.05))
    wb.add("virtual_cell", VirtualCell(n_genes=20, seed=42))
    wb.add("translator", ExpressionTranslator(base_current=8.0))
    wb.add("expr_mon", ExpressionMonitor())
    wb.add("neuron", IzhikevichPopulation(n=5, preset="RS", sample_indices=[0]))
    wb.add("spike_mon", SpikeMonitor(max_neurons=5))
    wb.add("rate_mon", RateMonitor(n_neurons=5))
    wb.add("metrics", NeuroMetrics(n_neurons=5))

    wb.connect("perturbation.perturbation", ["virtual_cell.perturbation"])
    wb.connect("virtual_cell.expression_profile", ["translator.expression_profile", "expr_mon.expression_profile"])
    wb.connect("translator.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["spike_mon.spikes", "rate_mon.spikes", "metrics.spikes"])
    wb.apply()

    world.run(duration=0.2, tick_dt=0.001)
    visuals = world.collect_visuals()
    assert len(visuals) > 0

    # Should have visuals from VirtualCell, ExpressionTranslator,
    # ExpressionMonitor, IzhikevichPopulation, SpikeMonitor, etc.
    module_names = [v["module"] for v in visuals]
    assert "VirtualCell" in module_names
    assert "ExpressionTranslator" in module_names
