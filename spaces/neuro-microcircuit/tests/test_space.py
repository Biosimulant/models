from __future__ import annotations


def test_space_runs(bsim):
    from src.poisson_input import PoissonInput
    from src.izhikevich import IzhikevichPopulation
    from src.exp_synapse import ExpSynapseCurrent
    from src.spike_monitor import SpikeMonitor
    from src.rate_monitor import RateMonitor
    from src.state_monitor import StateMonitor
    from src.neuro_metrics import NeuroMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("poisson", PoissonInput(n=40, rate_hz=15.0, seed=42))
    wb.add("exc", IzhikevichPopulation(n=40, preset="RS", sample_indices=[0, 1, 2]))
    wb.add("inh", IzhikevichPopulation(n=10, preset="FS", sample_indices=[0]))

    wb.add("syn_ext_e", ExpSynapseCurrent(n_pre=40, n_post=40, p_connect=0.1, weight=1.0, tau=0.005, seed=42))
    wb.add("syn_ee", ExpSynapseCurrent(n_pre=40, n_post=40, p_connect=0.1, weight=0.3, tau=0.005, seed=43))
    wb.add("syn_ei", ExpSynapseCurrent(n_pre=40, n_post=10, p_connect=0.1, weight=0.5, tau=0.005, seed=44))
    wb.add("syn_ie", ExpSynapseCurrent(n_pre=10, n_post=40, p_connect=0.1, weight=-1.5, tau=0.010, seed=45))
    wb.add("syn_ii", ExpSynapseCurrent(n_pre=10, n_post=10, p_connect=0.1, weight=-0.5, tau=0.010, seed=46))

    wb.add("spike_mon_e", SpikeMonitor(max_neurons=40))
    wb.add("spike_mon_i", SpikeMonitor(max_neurons=10, height=100))
    wb.add("rate_mon", RateMonitor(window_size=0.02, n_neurons=50))
    wb.add("state_mon", StateMonitor(max_points=200))
    wb.add("metrics", NeuroMetrics(n_neurons=50))

    wb.connect("poisson.spikes", ["syn_ext_e.spikes"])
    wb.connect("syn_ext_e.current", ["exc.current"])
    wb.connect("exc.spikes", ["syn_ee.spikes", "syn_ei.spikes", "spike_mon_e.spikes", "rate_mon.spikes", "metrics.spikes"])
    wb.connect("exc.state", ["state_mon.state"])
    wb.connect("inh.spikes", ["syn_ie.spikes", "syn_ii.spikes", "spike_mon_i.spikes", "rate_mon.spikes", "metrics.spikes"])
    wb.connect("syn_ee.current", ["exc.current"])
    wb.connect("syn_ie.current", ["exc.current"])
    wb.connect("syn_ei.current", ["inh.current"])
    wb.connect("syn_ii.current", ["inh.current"])
    wb.apply()

    world.run(duration=0.01, tick_dt=0.0001)
    assert "rate_state" in world.get_outputs("rate_mon")
    assert "metrics" in world.get_outputs("metrics")

