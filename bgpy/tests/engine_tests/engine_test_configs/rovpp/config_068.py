from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_010
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn, ROVPPV2aSimpleAS


config_068 = EngineTestConfig(
    name="068",
    desc="ROV++ v2a adopting AS 2. It is not useful in this type of attack",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({2: ROVPPV2aSimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    as_graph_info=as_graph_info_010,
)
