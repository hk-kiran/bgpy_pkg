from frozendict import frozendict
from bgpy.enums import ASNs
from .as_graph_info_000 import as_graph_info_000
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGP, RouteFlapDampening
from bgpy.simulation_framework import (
    ScenarioConfig,
    RouteFlapAttack,
    preprocess_anns_funcs,
)


desc = (
    "Route Flap attack by 666\n"
    "Route Flap Dampening Defense Policy, sparse adoption"

)

ex_config_031 = EngineTestConfig(
    name="ex_031_route_flap_attack_and_route_flap_dampening_policy",
    desc=desc,
    scenario_config=ScenarioConfig(
        ScenarioCls=RouteFlapAttack,
        preprocess_anns_func=preprocess_anns_funcs.noop,
        BasePolicyCls=BGP,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: RouteFlapDampening,
                # 1: RouteFlapDampening,
                ASNs.ATTACKER.value: BGP,
            }
        ),
    ),
    as_graph_info=as_graph_info_000,
)
