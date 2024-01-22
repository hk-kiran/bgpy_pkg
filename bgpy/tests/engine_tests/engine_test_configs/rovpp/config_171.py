from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_036
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn

config_171 = EngineTestConfig(
    name="171",
    desc="Subprefix Hijack Attack with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                5: ROVSimpleAS,
                8: ROVSimpleAS,
                10: ROVSimpleAS,
                15: ROVSimpleAS,
                ASNs.VICTIM.value: ROVSimpleAS,
            }
        ),
    ),
    as_graph_info=as_graph_info_036,
    propagation_rounds=1,
)
