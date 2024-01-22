from frozendict import frozendict
from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_012
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn, ROVPPV1SimpleAS

config_128 = EngineTestConfig(
    name="128",
    desc="Superprefix+Prefix Attack on Prefix with v1",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {2: ROVPPV1SimpleAS, 4: ROVPPV1SimpleAS, 11: ROVPPV1SimpleAS}
        ),
    ),
    as_graph_info=as_graph_info_012,
    propagation_rounds=1,
)
