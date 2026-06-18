"""
Aryan — graph_queries.py
Common graph traversal queries for the knowledge graph.
"""
import json
from pathlib import Path
import networkx as nx


def load_graph(path: str = "./knowledge_graph/graph.json") -> nx.DiGraph:
    if not Path(path).exists():
        return nx.DiGraph()
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
    return sorted(set(vendors))


def get_all_nodes_by_type(G: nx.DiGraph, node_type: str) -> list[dict]:
    return [{"id": n, **G.nodes[n]} for n in G.nodes if G.nodes[n].get("type") == node_type]


def get_documents_for_entity(G: nx.DiGraph, entity_id: str) -> list[dict]:
    """Return document nodes directly connected to a truck, driver, or trailer."""
    if entity_id not in G:
        return []

    docs = []
    for _, target, edge in G.out_edges(entity_id, data=True):
        if edge.get("relation") in {"has_document", "associated_with"}:
            if G.nodes[target].get("type") == "document":
                docs.append({"id": target, **G.nodes[target], "relation": edge.get("relation")})
    return docs


def get_trailers_for_truck(G: nx.DiGraph, truck_id: str) -> list[dict]:
    """Infer truck-trailer links through shared source documents."""
    truck_docs = {doc["id"] for doc in get_documents_for_entity(G, truck_id)}
    if not truck_docs:
        return []

    trailers = []
    for trailer in get_all_nodes_by_type(G, "trailer"):
        trailer_docs = {doc["id"] for doc in get_documents_for_entity(G, trailer["id"])}
        shared_docs = sorted(truck_docs & trailer_docs)
        if shared_docs:
            trailers.append({**trailer, "shared_document_ids": shared_docs})
    return trailers


def get_relationship_context(G: nx.DiGraph, entity_id: str, depth: int = 2) -> dict:
    """Small, serializable graph context for hybrid/RAG explanations."""
    if entity_id not in G:
        return {"nodes": [], "edges": []}

    seen = {entity_id}
    frontier = {entity_id}
    for _ in range(max(depth, 0)):
        next_frontier = set()
        for node in frontier:
            next_frontier.update(G.successors(node))
            next_frontier.update(G.predecessors(node))
        next_frontier -= seen
        seen.update(next_frontier)
        frontier = next_frontier

    sub = G.subgraph(seen)
    return {
        "nodes": [{"id": n, **G.nodes[n]} for n in sub.nodes],
        "edges": [{"source": u, "target": v, **d} for u, v, d in sub.edges(data=True)],
    }
