"""
Charan — entity_linker.py
Links extracted metadata to existing Truck, Driver, Trailer records in the DB.
Returns IDs to store on the Document row.
"""
from sqlalchemy.orm import Session
from backend.database.models import Truck, Driver, Trailer


def link_entities(meta: dict, db: Session) -> dict:
    """
    Given Claude-extracted metadata, resolve to DB entity IDs.

    Returns:
        { "truck_id": str|None, "driver_id": str|None, "trailer_id": str|None }
    """
    return {
        "truck_id": _resolve_truck(meta.get("truck_unit_number"), db),
        "driver_id": _resolve_driver(meta.get("driver_name"), db),
        "trailer_id": _resolve_trailer(meta.get("trailer_unit_number"), db),
    }


def _resolve_truck(unit_number: int | None, db: Session) -> str | None:
    if unit_number is None:
        return None
    truck = db.query(Truck).filter(Truck.unit_number == unit_number).first()
    return truck.id if truck else None


def _resolve_driver(name: str | None, db: Session) -> str | None:
    if not name:
        return None
    # Fuzzy match on full name — case insensitive
    driver = db.query(Driver).filter(
        Driver.name.ilike(f"%{name.strip()}%")
    ).first()
    return driver.id if driver else None


def _resolve_trailer(unit_number: int | None, db: Session) -> str | None:
    if unit_number is None:
        return None
    trailer = db.query(Trailer).filter(Trailer.unit_number == unit_number).first()
    return trailer.id if trailer else None
