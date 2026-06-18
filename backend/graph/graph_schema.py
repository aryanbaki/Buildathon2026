"""
Aryan — graph_schema.py
Defines node and edge types for the fleet knowledge graph.
"""

NODE_TYPES = {
    "truck":    {"color": "#534AB7", "shape": "square"},
    "driver":   {"color": "#0F6E56", "shape": "circle"},
    "document": {"color": "#854F0B", "shape": "diamond"},
    "vendor":   {"color": "#993C1D", "shape": "triangle"},
    "trailer":  {"color": "#185FA5", "shape": "square"},
}

EDGE_TYPES = {
    "has_document":    {"label": "has document", "color": "#888780"},
    "associated_with": {"label": "associated with", "color": "#5DCAA5"},
    "serviced_by":     {"label": "serviced by", "color": "#D85A30"},
    "assigned_to":     {"label": "assigned to", "color": "#7F77DD"},
    "has_maintenance": {"label": "has maintenance", "color": "#A65F00"},
    "has_fuel_record": {"label": "has fuel record", "color": "#2F7D32"},
    "documented_by":   {"label": "documented by", "color": "#69707D"},
}
