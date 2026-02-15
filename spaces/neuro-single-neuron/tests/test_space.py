from __future__ import annotations


def test_space_runs(bsim):
    from src.step_current import StepCurrent
    from src.izhikevich import IzhikevichPopulation
    from src.spike_monitor import SpikeMonitor
    from src.state_monitor import StateMonitor
    from src.neuro_metrics import NeuroMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("current", StepCurrent(I=10.0))
    wb.add("neuron", IzhikevichPopulation(n=1, preset="RS", sample_indices=[0]))
    wb.add("spike_mon", SpikeMonitor(max_neurons=1))
    wb.add("state_mon", StateMonitor(max_points=100))
    wb.add("metrics", NeuroMetrics(n_neurons=1))

    wb.connect("current.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["spike_mon.spikes", "metrics.spikes"])
    wb.connect("neuron.state", ["state_mon.state"])
    wb.apply()

    world.run(duration=0.02, tick_dt=0.001)

    # Monitors/metrics should emit real signals.
    assert "spike_summary" in world.get_outputs("spike_mon")
    assert "voltage_summary" in world.get_outputs("state_mon")
    assert "metrics" in world.get_outputs("metrics")

