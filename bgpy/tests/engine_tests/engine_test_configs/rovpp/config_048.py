from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_008
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPV2aLiteSimpleAS, ROVPPAnn


config_048 = EngineTestConfig(
    name="048",
    desc=(
        "Subprefix Hijack that tests blackhole announcements should "
        "be sent, even if hijack comes from a customer with ROV++ v2a "
        "lite. This comes with the added check to see if it gets sent to peers."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aLiteSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({1: ROVPPV2aLiteSimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    as_graph_info=as_graph_info_008,
)
