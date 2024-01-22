from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_023
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn
from bgpy.simulation_engine.policies.rovpp import ROVPPV2SimpleAS

config_195 = EngineTestConfig(
    name="195",
    desc="",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                4: ROVPPV2SimpleAS,
                10: ROVPPV2SimpleAS,
                ASNs.VICTIM.value: ROVPPV2SimpleAS,
            }
        ),
    ),
    as_graph_info=as_graph_info_023,
    propagation_rounds=1,
)
