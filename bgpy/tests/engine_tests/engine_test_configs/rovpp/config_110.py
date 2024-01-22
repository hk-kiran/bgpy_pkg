from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_049
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixPrefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn
from bgpy.simulation_engine.policies.rovpp import ROVPPV2aSimpleAS


config_110 = EngineTestConfig(
    name="110",
    desc="Superprefix+Prefix Attack on NonRouted Prefix with v2a",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({4: ROVPPV2aSimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    as_graph_info=as_graph_info_049,
    propagation_rounds=1,
)
