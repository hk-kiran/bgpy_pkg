from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_018
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn, ROVPPV2ShortenSimpleAS

config_220 = EngineTestConfig(
    name="220",
    desc="Non routed prefix attack with v2_journal",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2ShortenSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({3}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ROVPPV2ShortenSimpleAS,
            }
        ),
    ),
    as_graph_info=as_graph_info_018,
    propagation_rounds=1,
)
