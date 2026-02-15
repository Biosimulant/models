from __future__ import annotations


def test_space_runs(bsim):
    from src.step_current import StepCurrent
    from src.hodgkin_huxley import HodgkinHuxleyPopulation
    from src.spike_monitor import SpikeMonitor
    from src.state_monitor import StateMonitor
    from src.hodgkin_huxley_monitor import HHStateMonitor
    from src.neuro_metrics import NeuroMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("current", StepCurrent(I=10.0))
    wb.add("neuron", HodgkinHuxleyPopulation(n=1, sample_indices=[0]))
    wb.add("spike_mon", SpikeMonitor(max_neurons=1))
    wb.add("state_mon", StateMonitor(max_points=200))
    wb.add("hh_mon", HHStateMonitor(max_points=200, neuron_index=0))
    wb.add("metrics", NeuroMetrics(n_neurons=1))

    wb.connect("current.current", ["neuron.current"])
    wb.connect("neuron.spikes", ["spike_mon.spikes", "metrics.spikes"])
    wb.connect("neuron.state", ["state_mon.state", "hh_mon.state"])
    wb.apply()

    world.run(duration=0.01, tick_dt=0.0001)
    assert "hh_state_summary" in world.get_outputs("hh_mon")

