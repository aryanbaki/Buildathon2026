"""
Aryan — graph_builder.py
Builds a NetworkX knowledge graph linking trucks → documents → drivers → vendors.
Exports to knowledge_graph/graph.json for GraphView.jsx.
"""
import json
import os
import networkx as nx
from sqlalchemy.orm import Session

from backend.database.models import Truck, Driver, Document, MaintenanceRecord


def build_graph(db: Session) -> nx.DiGraph:
    G = nx.DiGraph()

    trucks = db.query(Truck).all()
    for t in trucks:
        G.add_node(t.id, label=f"Truck {t.unit_number}", type="truck",
                   make=t.make, model=t.model, year=t.year, status=t.status)

    drivers = db.query(Driver).all()
    for d in drivers:
        G.add_node(d.id, label=d.name, type="driver", status=d.status)

    docs = db.query(Document).all()
    for doc in docs:
        G.add_node(doc.id, label=doc.filename, type="document",
                   doc_type=doc.doc_type.value if doc.doc_type else "other",
                   amount=doc.amount, doc_date=str(doc.doc_date) if doc.doc_date else None)
        if doc.truck_id:
            G.add_edge(doc.truck_id, doc.id, relation="has_document")
        if doc.driver_id:
            G.add_edge(doc.driver_id, doc.id, relation="associated_with")
        if doc.vendor:
            vendor_node = f"vendor_{doc.vendor}"
            G.add_node(vendor_node, label=doc.vendor, type="vendor")
            G.add_edge(doc.id, vendor_node, relation="serviced_by")

    return G


def export_graph(G: nx.DiGraph, output_path: str = "./knowledge_graph/graph.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = nx.node_link_data(G)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return output_path


def rebuild_graph(db: Session) -> str:
    G = build_graph(db)
    return export_graph(G)
