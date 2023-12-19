"""Gontains functions needed to build graph and it's references"""

from typing import TYPE_CHECKING

from .base_as import AS

if TYPE_CHECKING:
    from bgpy.as_graphs import ASGraphInfo
    from bgpy.simulation_engine import BGPSimplePolicy


def _gen_graph(
    self,
    as_graph_info: ASGraphInfo,
    BaseASCls: type[AS],
    BasePolicyCls: type["BGPSimplePolicy"],
):
    """Generates a graph of AS objects"""

    def _gen_as(asn):
        as_ = BaseASCls(
            asn,
            policy=BasePolicyCls(),
        )
        assert as_.policy.as_ == as_, f"{BaseASCls} not setting policy.as_ correctly"
        # Monkey patching these in here whilst generating the AS graph
        as_.peers_setup_set = set()
        as_.customers_setup_set = set()
        as_.providers_setup_set = set()
        return as_

    # Add all links to the graph
    for asn in as_graph_info.asns:
        self.as_dict[asn] = self.as_dict.get(asn, _gen_as(asn))

    # Add all IXPs to the graph
    for asn in as_graph_info.ixp_asns:
        self.as_dict[asn] = self.as_dict.get(asn, _gen_as(asn))
        self.as_dict[asn].ixp = True

    # Add all input cliques to the graph
    for asn in as_graph_info.input_clique_asns:
        self.as_dict[asn] = self.as_dict.get(asn, _gen_as(asn))
        self.as_dict[asn].input_clique = True


def _add_relationships(self, as_graph_info: ASGraphInfo) -> None:
    """Adds relationships to the graph as references

    NOTE: we monkey patch peers_setup_set while the AS Graph is being generated
    for speed
    """

    for cp_link in as_graph_info.customer_provider_links:
        # Extract customer and provider obj
        customer = self.as_dict[cp_link.customer_asn]
        provider = self.as_dict[cp_link.provider_asn]
        # Store references
        customer.providers_setup_set.add(provider)
        provider.customers_setup_set.add(customer)

    for peer_link in as_graph_info.peer_links:
        # Extract as objects for peers
        asn1, asn2 = peer_link.asns
        p1, p2 = self.as_dict[asn1], self.as_dict[asn2]
        # Add references to peers
        p1.peers_setup_set.add(p2)
        p2.peers_setup_set.add(p1)


def _make_relationships_tuples(self):
    """Make relationships tuples

    NOTE: we monkey patch peers_setup_set while the AS Graph is being generated
    for speed
    """

    rel_attrs = ("peers", "providers", "customers")
    setup_rel_attrs = ("peers_setup_set", "providers_setup_set", "customers_setup_set")

    for as_obj in self:
        for rel_attr, setup_rel_attr in zip(rel_attrs, setup_rel_attrs):
            # Conver the setup attribute to tuple
            setattr(as_obj, rel_attr, tuple(getattr(as_obj, setup_rel_attr)))
            # Delete the setup attribute
            delattr(as_obj, setup_rel_attr)
