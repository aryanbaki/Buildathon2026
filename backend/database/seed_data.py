"""
Charan — seed_data.py
Seeds fleet entities (trucks, drivers, trailers, assignments).
Documents come from bootstrap_fleet_data after running generate_documents.py.

Usage: python -m backend.database.seed_data
"""
from datetime import date

from backend.database.db import get_db, init_db
from backend.database.models import Truck, Driver, Trailer, DriverAssignment
from backend.database.fleet_fixtures import TRUCKS, DRIVERS, TRAILERS

ASSIGNMENTS = [
    dict(truck_id="truck_84", driver_id="driver_001", start_date=date(2022, 1, 1), is_primary=True),
    dict(truck_id="truck_85", driver_id="driver_002", start_date=date(2021, 3, 1), is_primary=True),
    dict(truck_id="truck_86", driver_id="driver_003", start_date=date(2022, 6, 1), end_date=date(2024, 12, 31), is_primary=True),
    dict(truck_id="truck_87", driver_id="driver_004", start_date=date(2021, 8, 1), is_primary=True),
    dict(truck_id="truck_88", driver_id="driver_002", start_date=date(2023, 3, 1), is_primary=True),
    dict(truck_id="truck_89", driver_id="driver_005", start_date=date(2022, 11, 1), is_primary=True),
    dict(truck_id="truck_90", driver_id="driver_001", start_date=date(2020, 5, 1), end_date=date(2021, 12, 31), is_primary=True),
    dict(truck_id="truck_91", driver_id="driver_004", start_date=date(2023, 6, 1), is_primary=True),
    dict(truck_id="truck_92", driver_id="driver_003", start_date=date(2020, 1, 1), end_date=date(2022, 5, 31), is_primary=True),
    dict(truck_id="truck_93", driver_id="driver_005", start_date=date(2024, 1, 1), is_primary=True),
]


def seed_entities(db=None):
    """Seed or update trucks, drivers, trailers, and assignments."""
    close_after = False
    if db is None:
        db = get_db().__enter__()
        close_after = True

    for td in TRUCKS:
        db.merge(Truck(**td))
    for dd in DRIVERS:
        db.merge(Driver(**dd))
    for td in TRAILERS:
        db.merge(Trailer(**td))

    db.query(DriverAssignment).delete()
    db.flush()

    for assignment in ASSIGNMENTS:
        db.add(DriverAssignment(**assignment))

    if close_after:
        db.commit()
        db.close()

    return {
        "trucks": len(TRUCKS),
        "drivers": len(DRIVERS),
        "trailers": len(TRAILERS),
        "assignments": len(ASSIGNMENTS),
    }


def seed():
    init_db()
    with get_db() as db:
        counts = seed_entities(db)
        print("Seed complete (entities only — run bootstrap for documents):")
        print(f"  {counts['trucks']} trucks")
        print(f"  {counts['drivers']} drivers")
        print(f"  {counts['trailers']} trailers")
        print(f"  {counts['assignments']} driver assignments")


if __name__ == "__main__":
    seed()
