from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_048
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixPrefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn

config_215 = EngineTestConfig(
    name="215",
    desc="Superprefix+Prefix Attack on NonRouted Prefix with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                3: ROVSimpleAS,
                4: ROVSimpleAS,
                6: ROVSimpleAS,
            }
        ),
    ),
    as_graph_info=as_graph_info_048,
    propagation_rounds=1,
)
