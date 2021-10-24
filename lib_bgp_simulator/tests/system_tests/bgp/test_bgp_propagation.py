import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from ..utils import run_example, HijackLocalRIB

from ....announcements import AnnWDefaults
from ....enums import ASNs, Relationships as Rels, ROAValidity
from ....engine_input import SubprefixHijack

from ....engine import BGPSimpleAS
from ....engine import BGPAS
from ....engine import LocalRIB

@pytest.mark.parametrize("BaseASCls", [BGPSimpleAS, BGPAS])
def test_propagate_bgp(BaseASCls):
    r"""
    Test propagating up without multihomed support in the following test graph.
    Horizontal lines are peer relationships, vertical lines are customer-provider.

      1
      |
      2---3
     /|    \
    4 5--6  7

    Starting propagation at 5, all ASes should see the announcement.
    """
    # Graph data
    peers = [PeerLink(2, 3), PeerLink(5, 6)]
    customer_providers = [CPLink(provider_asn=1, customer_asn=2),
                          CPLink(provider_asn=2, customer_asn=5),
                          CPLink(provider_asn=2, customer_asn=4),
                          CPLink(provider_asn=3, customer_asn=7)]
    # Number identifying the type of AS class
    as_policies = {asn: BaseASCls for asn in
                   list(range(1, 8))}

    # Announcements
    prefix = '137.99.0.0/16'
    announcements = [AnnWDefaults(prefix=prefix, as_path=(5,),timestamp=0, seed_asn=5,
                                  roa_validity=ROAValidity.UNKNOWN,
                                  recv_relationship=Rels.ORIGIN,
                                  traceback_end=True)]

    kwargs = {"prefix": prefix, "timestamp": 0, "roa_validity": ROAValidity.UNKNOWN,
                      "traceback_end": False}

    # Local RIB data
    local_ribs = {
        1: ({prefix: AnnWDefaults(as_path=(1, 2, 5), recv_relationship=Rels.CUSTOMERS, **kwargs)}),
        2: ({prefix: AnnWDefaults(as_path=(2, 5), recv_relationship=Rels.CUSTOMERS, **kwargs)}),
        3: ({prefix: AnnWDefaults(as_path=(3, 2, 5), recv_relationship=Rels.PEERS, **kwargs)}),
        4: ({prefix: AnnWDefaults(as_path=(4, 2, 5), recv_relationship=Rels.PROVIDERS, **kwargs)}),
        5: ({prefix: announcements[0]}),
        6: ({prefix: AnnWDefaults(as_path=(6, 5), recv_relationship=Rels.PEERS, **kwargs)}),
        7: ({prefix: AnnWDefaults(as_path=(7, 3, 2, 5), recv_relationship=Rels.PROVIDERS, **kwargs)}),
    }

    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=announcements,
                local_ribs=local_ribs)
