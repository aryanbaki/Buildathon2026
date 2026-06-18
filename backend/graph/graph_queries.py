"""
Aryan — graph_queries.py
Common graph traversal queries for the knowledge graph.
"""
import json
import networkx as nx


def load_graph(path: str = "./knowledge_graph/graph.json") -> nx.DiGraph:
    with open(path) as f:
        data = json.load(f)
    return nx.node_link_graph(data, directed=True)


def get_truck_subgraph(G: nx.DiGraph, truck_id: str) -> dict:
    """Return all nodes reachable from a truck node."""
    if truck_id not in G:
        return {"nodes": [], "edges": []}
    reachable = nx.descendants(G, truck_id) | {truck_id}
    sub = G.subgraph(reachable)
    return {
        "nodes": [{"id": n, **G.nodes[n]} for n in sub.nodes],
        "edges": [{"source": u, "target": v, **d} for u, v, d in sub.edges(data=True)],
    }


def get_vendors_for_truck(G: nx.DiGraph, truck_id: str) -> list[str]:
    vendors = []
    for node in nx.descendants(G, truck_id):
        if G.nodes[node].get("type") == "vendor":
            vendors.append(G.nodes[node].get("label", node))
    return vendors


def get_all_nodes_by_type(G: nx.DiGraph, node_type: str) -> list[dict]:
    return [{"id": n, **G.nodes[n]} for n in G.nodes if G.nodes[n].get("type") == node_type]
