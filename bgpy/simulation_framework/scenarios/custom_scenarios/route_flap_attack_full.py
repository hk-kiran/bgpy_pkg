from typing import Optional, TYPE_CHECKING
from bgpy.simulation_framework.scenarios.roa_info import ROAInfo
import random
from bgpy.enums import SpecialPercentAdoptions, Timestamps, Prefixes
from ..scenario import Scenario


if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann
    from bgpy.simulation_engine import BaseSimulationEngine


class RouteFlapAttackFull(Scenario):
    """Route flap attack engine input"""
    min_propagation_rounds = 5
    random_flapping = True

    def _get_announcements(self, *args, **kwargs) -> tuple["Ann", ...]:
        """Returns the two announcements seeded for this engine input

        This engine input is for a prefix hijack,
        consisting of a valid prefix and invalid prefix

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """
        anns = list()
        for victim_asn in self.victim_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(victim_asn,),
                    timestamp=Timestamps.VICTIM.value,
                )
            )

        for attacker_asn in self.attacker_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(attacker_asn,),
                    timestamp=Timestamps.ATTACKER.value,
                )
            )

        return tuple(anns)
    
    def _get_roa_infos(
        self,
        *,
        announcements: tuple["Ann", ...] = (),
        engine: Optional["BaseSimulationEngine"] = None,
        prev_scenario: Optional["Scenario"] = None,
    ) -> tuple[ROAInfo, ...]:
        """Returns a tuple of ROAInfo's"""

        return tuple([ROAInfo(Prefixes.PREFIX.value, x) for x in self.victim_asns])
    
    def post_propagation_hook(
        self,
        engine: "BaseSimulationEngine",
        percent_adopt: float | SpecialPercentAdoptions,
        trial: int,
        propagation_round: int,
    ) -> None:
        if propagation_round == self.min_propagation_rounds - 1:
            return
        elif propagation_round >= self.min_propagation_rounds:
            raise NotImplementedError
        announcements: list["Ann"] = list(self.announcements)  # type: ignore
        for attacker_asn in self.attacker_asns:
                for prefix, ann in engine.as_graph.as_dict[
                    attacker_asn
                ].policy._local_rib.items():
                    announcements.remove(
                        ann
                    )
                    announcements.append(
                        ann.copy(
                            {
                            "no_of_times_announced": 
                            (ann.no_of_times_announced + random.randint(0, 1))
                              if self.random_flapping 
                              else (ann.no_of_times_announced + 1)
                            }
                        )
                    )

        self.announcements = tuple(announcements)
        self.setup_engine(engine)
        engine.ready_to_run_round = propagation_round+1
