from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_004
from bgpy.tests.engine_tests.utils import EngineTestConfig
from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPV2aSimpleAS, ROVPPAnn

config_043 = EngineTestConfig(
    name="043",
    desc=(
        "Subprefix Hijack from fig 3a in paper with ROV++ v2a "
        "adopting at AS 4 and 8, and ROV at 7. ASes 4, 8, "
        "and 7 should be disconnected"
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {4: ROVPPV2aSimpleAS, 7: ROVSimpleAS, 8: ROVPPV2aSimpleAS}
        ),
    ),
    as_graph_info=as_graph_info_004,
)
