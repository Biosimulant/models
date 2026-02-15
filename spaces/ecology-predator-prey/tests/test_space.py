from __future__ import annotations


def test_space_runs(bsim):
    from src.environment import Environment
    from src.organism_population import OrganismPopulation
    from src.predator_prey import PredatorPreyInteraction
    from src.population_monitor import PopulationMonitor
    from src.phase_space import PhaseSpaceMonitor
    from src.ecology_metrics import EcologyMetrics

    world = bsim.BioWorld()
    wb = bsim.WiringBuilder(world)

    wb.add("environment", Environment(temperature=20.0, water=80.0, food_availability=1.0, sunlight=1.0, seasonal_cycle=False))
    wb.add("rabbits", OrganismPopulation(name="Rabbits", initial_count=80, birth_rate=0.10, death_rate=0.02, carrying_capacity=200, seed=42))
    wb.add("foxes", OrganismPopulation(name="Foxes", initial_count=10, birth_rate=0.04, death_rate=0.02, carrying_capacity=50, seed=43))
    wb.add("predation", PredatorPreyInteraction(predation_rate=0.01, conversion_efficiency=1.0, seed=44))
    wb.add("pop_monitor", PopulationMonitor(max_points=100))
    wb.add("phase_space", PhaseSpaceMonitor(x_species="Rabbits", y_species="Foxes", max_points=100))
    wb.add("metrics", EcologyMetrics())

    wb.connect("environment.conditions", ["rabbits.conditions", "foxes.conditions"])
    wb.connect("rabbits.population_state", ["predation.prey_state", "pop_monitor.population_state", "phase_space.population_state", "metrics.population_state"])
    wb.connect("foxes.population_state", ["predation.predator_state", "pop_monitor.population_state", "phase_space.population_state", "metrics.population_state"])
    wb.connect("predation.predation", ["rabbits.predation"])
    wb.connect("predation.food_gained", ["foxes.food_gained"])
    wb.apply()

    world.run(duration=5.0, tick_dt=1.0)
    assert "metrics" in world.get_outputs("metrics")
    assert "population_summary" in world.get_outputs("pop_monitor")

