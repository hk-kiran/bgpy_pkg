from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_006
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixPrefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn
from bgpy.simulation_engine.policies.rovpp import ROVPPV2SimpleAS


config_101 = EngineTestConfig(
    name="101",
    desc="Superprefix+prefix Attack on NonRouted Prefix with v2",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({2: ROVPPV2SimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    as_graph_info=as_graph_info_006,
    propagation_rounds=1,
)
