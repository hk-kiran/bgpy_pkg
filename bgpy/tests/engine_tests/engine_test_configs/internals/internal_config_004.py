from frozendict import frozendict

from bgpy.as_graphs import PeerLink, CustomerProviderLink as CPLink
from bgpy.as_graphs import ASGraphInfo


from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import RouteFlapDampening
from bgpy.simulation_framework import (
    RouteFlapAttack,
    ScenarioConfig,
)

r"""Graph to test relationship preference

      2
     /
    1 - 3
     \
      4
     /
    5
"""

as_graph_info = ASGraphInfo(
    peer_links=frozenset([PeerLink(1, 3)]),
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=2, customer_asn=1),
            CPLink(provider_asn=1, customer_asn=4),
            CPLink(provider_asn=4, customer_asn=5),
        ]
    ),
)

internal_config_004 = EngineTestConfig(
    name="internal_004",
    desc="Test withdrawal mechanism caused by better announcement",
    scenario_config=ScenarioConfig(
        ScenarioCls=RouteFlapAttack,
        BasePolicyCls=RouteFlapDampening,
        override_victim_asns=frozenset({2}),
        override_attacker_asns=frozenset({3}),
        override_non_default_asn_cls_dict=frozendict(),
    ),
    as_graph_info=as_graph_info,
)
