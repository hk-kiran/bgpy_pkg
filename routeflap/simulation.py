from multiprocessing import cpu_count
from pathlib import Path

from bgpy.simulation_engine.policies import RouteFlapDampening, BGP
from bgpy.simulation_framework.scenarios import RouteFlapAttack

from bgpy.enums import SpecialPercentAdoptions
from bgpy.simulation_framework import Simulation, ScenarioConfig


def main():
    """Runs the defaults"""

    # Simulation for the paper
    sim = Simulation(
        percent_adoptions=(
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.4,
            0.8,
            0.99,  # SpecialPercentAdoptions.ALL_BUT_ONE,
        ),
        scenario_configs=(
            ScenarioConfig(ScenarioCls=RouteFlapAttack,
                            AdoptPolicyCls=BGP),
            ScenarioConfig(ScenarioCls=RouteFlapAttack, 
                            AdoptPolicyCls=RouteFlapDampening),
        ),
        output_dir=Path("/Simulation/routeflapattack").expanduser(),
        num_trials=100,
        parse_cpus=cpu_count(),
    )
    sim.run()


if __name__ == "__main__":
    # print("This takes about 6 minutes with PyPy")
    main()
