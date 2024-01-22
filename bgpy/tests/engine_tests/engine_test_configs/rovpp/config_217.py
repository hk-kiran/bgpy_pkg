from frozendict import frozendict

from bgpy.tests.engine_tests.as_graph_infos import as_graph_info_048
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixPrefixHijack

from bgpy.simulation_engine.policies.rovpp import ROVPPAnn, ROVPPV2SimpleAS

config_217 = EngineTestConfig(
    name="217",
    desc="Superprefix+Prefix Attack on NonRouted Prefix with v2",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                3: ROVPPV2SimpleAS,
                4: ROVPPV2SimpleAS,
                6: ROVPPV2SimpleAS,
            }
        ),
    ),
    as_graph_info=as_graph_info_048,
    propagation_rounds=1,
)
