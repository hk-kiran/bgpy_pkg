from abc import ABC, abstractmethod
from collections import defaultdict

import ipaddress
from ..attacker_success_subgraph import AttackerSuccessSubgraph
from .....enums import Outcomes
from .....engine import BGPAS


class AttackerSuccessAdoptingInputCliqueSubgraph(AttackerSuccessSubgraph):
    """Graph with attacker success for adopting input clique ASes"""

    def _get_subgraph_key(self, scenario, *args):
        """Returns the key to be used in shared_data on the subgraph"""

        return self._get_as_type_pol_outcome_perc_k(
            ASTypes.INPUT_CLIQUE, scenario.AdoptASCls, Outcomes.ATTACKER_SUCCESS)
