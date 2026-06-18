"""
Aryan — graph_builder.py
Builds a NetworkX knowledge graph linking trucks, drivers, trailers,
documents, vendors, maintenance, and fuel records.
Exports to knowledge_graph/graph.json for GraphView.jsx.
"""
import json
import os
import networkx as nx
from sqlalchemy.orm import Session

from backend.database.models import (
    Driver, DriverAssignment, Document, FuelRecord,
    MaintenanceRecord, Trailer, Truck
)


def build_graph(db: Session) -> nx.DiGraph:
    G = nx.DiGraph()

    trucks = db.query(Truck).all()
    for t in trucks:
        G.add_node(t.id, label=f"Truck {t.unit_number}", type="truck",
                   make=t.make, model=t.model, year=t.year, status=t.status)

    drivers = db.query(Driver).all()
    for d in drivers:
        G.add_node(d.id, label=d.name, type="driver", status=d.status)

    trailers = db.query(Trailer).all()
    for trailer in trailers:
        G.add_node(
            trailer.id,
            label=f"Trailer {trailer.unit_number}",
            type="trailer",
            trailer_type=trailer.trailer_type,
            license_plate=trailer.license_plate,
            state=trailer.state,
            status=trailer.status,
        )

    assignments = db.query(DriverAssignment).all()
    for assignment in assignments:
        if assignment.truck_id and assignment.driver_id:
            G.add_edge(
                assignment.driver_id,
                assignment.truck_id,
                relation="assigned_to",
                start_date=str(assignment.start_date),
                end_date=str(assignment.end_date) if assignment.end_date else None,
                is_primary=assignment.is_primary,
            )

    docs = db.query(Document).all()
    for doc in docs:
        G.add_node(doc.id, label=doc.filename, type="document",
                   doc_type=doc.doc_type.value if doc.doc_type else "other",
                   amount=doc.amount, doc_date=str(doc.doc_date) if doc.doc_date else None)
        if doc.truck_id:
            G.add_edge(doc.truck_id, doc.id, relation="has_document")
        if doc.driver_id:
            G.add_edge(doc.driver_id, doc.id, relation="associated_with")
        if doc.trailer_id:
            G.add_edge(doc.trailer_id, doc.id, relation="has_document")
        if doc.vendor:
            vendor_node = f"vendor_{doc.vendor}"
            G.add_node(vendor_node, label=doc.vendor, type="vendor")
            G.add_edge(doc.id, vendor_node, relation="serviced_by")

    for record in db.query(MaintenanceRecord).all():
        node_id = f"maintenance_{record.id}"
        G.add_node(
            node_id,
            label=record.service_type or "Maintenance",
            type="maintenance",
            vendor=record.vendor,
            total_cost=record.total_cost,
            service_date=str(record.service_date) if record.service_date else None,
        )
        if record.truck_id:
            G.add_edge(record.truck_id, node_id, relation="has_maintenance")
        if record.document_id:
            G.add_edge(node_id, record.document_id, relation="documented_by")

    for record in db.query(FuelRecord).all():
        node_id = f"fuel_{record.id}"
        G.add_node(
            node_id,
            label=record.location or "Fuel record",
            type="fuel",
            total_cost=record.total_cost,
            gallons=record.gallons,
            fill_date=str(record.fill_date) if record.fill_date else None,
        )
        if record.truck_id:
            G.add_edge(record.truck_id, node_id, relation="has_fuel_record")
        if record.document_id:
            G.add_edge(node_id, record.document_id, relation="documented_by")

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
