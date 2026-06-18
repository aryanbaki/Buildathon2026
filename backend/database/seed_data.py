"""
Charan — seed_data.py
Seeds the database with trucks, drivers, trailers, and links synthetic documents.
Run once after init_db().

Usage: python -m backend.database.seed_data
"""
import os
import uuid
from datetime import date, timedelta
import random

from backend.database.db import get_db, init_db
from backend.database.models import (
    Truck, Driver, Trailer, DriverAssignment,
    Document, MaintenanceRecord, FuelRecord, DocType
)

random.seed(42)


def seed():
    init_db()
    with get_db() as db:
        # --- Trucks ---
        trucks_data = [
            dict(id="truck_84", unit_number=84, vin="1FUJGEBG0JLGE1234",
                 make="Freightliner", model="Cascadia", year=2019,
                 license_plate="TX-84FLT", state="TX", status="active",
                 purchase_date=date(2019, 3, 15), purchase_price=145000, odometer=312000),
            dict(id="truck_85", unit_number=85, vin="1XKYDP9X4LJ123456",
                 make="Kenworth", model="T680", year=2020,
                 license_plate="TX-85FLT", state="TX", status="active",
                 purchase_date=date(2020, 7, 1), purchase_price=162000, odometer=198000),
            dict(id="truck_86", unit_number=86, vin="1XPBD49X4JD123789",
                 make="Peterbilt", model="579", year=2018,
                 license_plate="TX-86FLT", state="TX", status="inactive",
                 purchase_date=date(2018, 11, 20), purchase_price=138000, odometer=487000),
        ]
        trucks = []
        for td in trucks_data:
            t = Truck(**td)
            db.merge(t)
            trucks.append(t)

        # --- Drivers ---
        drivers_data = [
            dict(id="driver_001", name="Carlos Mendez", cdl_number="TX-CDL-7734221",
                 cdl_expiry=date(2027, 6, 30), phone="214-555-0101",
                 email="cmendez@fleet.com", hire_date=date(2020, 2, 1), status="active"),
            dict(id="driver_002", name="James Whitfield", cdl_number="TX-CDL-8821045",
                 cdl_expiry=date(2026, 9, 15), phone="972-555-0188",
                 email="jwhitfield@fleet.com", hire_date=date(2019, 8, 15), status="active"),
            dict(id="driver_003", name="Maria Santos", cdl_number="TX-CDL-9934512",
                 cdl_expiry=date(2025, 12, 31), phone="469-555-0234",
                 email="msantos@fleet.com", hire_date=date(2021, 5, 10), status="active"),
        ]
        drivers = []
        for dd in drivers_data:
            d = Driver(**dd)
            db.merge(d)
            drivers.append(d)

        # --- Trailers ---
        trailers_data = [
            dict(id="trailer_01", unit_number=101, trailer_type="Dry Van",
                 capacity_tons=22.0, license_plate="TX-T101", state="TX", status="active"),
            dict(id="trailer_02", unit_number=102, trailer_type="Reefer",
                 capacity_tons=20.0, license_plate="TX-T102", state="TX", status="active"),
        ]
        for td in trailers_data:
            db.merge(Trailer(**td))

        db.flush()

        # --- Driver assignments ---
        assignments = [
            dict(truck_id="truck_84", driver_id="driver_001", start_date=date(2022, 1, 1), is_primary=True),
            dict(truck_id="truck_85", driver_id="driver_002", start_date=date(2021, 3, 1), is_primary=True),
            dict(truck_id="truck_86", driver_id="driver_003", start_date=date(2022, 6, 1), end_date=date(2024, 12, 31), is_primary=True),
        ]
        for a in assignments:
            db.add(DriverAssignment(**a))

        # --- Documents + Maintenance + Fuel records ---
        def ago(days):
            return date.today() - timedelta(days=days)

        doc_seeds = [
            # Truck 84
            dict(id=str(uuid.uuid4()), truck_id="truck_84", doc_type=DocType.REGISTRATION,
                 filename="registration.txt", doc_date=ago(180), expiry_date=ago(180) + timedelta(365),
                 extracted_metadata={"doc_type": "registration"}, confidence_score=0.95),
            dict(id=str(uuid.uuid4()), truck_id="truck_84", doc_type=DocType.TAX_FORM,
                 filename="form_2290_2025.txt", doc_date=date(2025, 8, 31),
                 extracted_metadata={"doc_type": "tax_form", "amount": 550}, amount=550, confidence_score=0.97),
            dict(id=str(uuid.uuid4()), truck_id="truck_84", driver_id="driver_001",
                 doc_type=DocType.MAINTENANCE, filename="maintenance_jan14.txt",
                 doc_date=ago(155), amount=1200, vendor="Dallas Fleet Services",
                 extracted_metadata={"service_type": "Brake Pad Replacement", "parts_cost": 720, "labor_cost": 480},
                 confidence_score=0.96),
            dict(id=str(uuid.uuid4()), truck_id="truck_84", driver_id="driver_001",
                 doc_type=DocType.FUEL_RECEIPT, filename="fuel_jan03.txt",
                 doc_date=ago(166), amount=380, vendor="Pilot Travel Center",
                 extracted_metadata={"gallons": 94.2, "price_per_gallon": 4.035}, confidence_score=0.98),
            dict(id=str(uuid.uuid4()), truck_id="truck_84", driver_id="driver_001",
                 doc_type=DocType.MAINTENANCE, filename="maintenance_mar08.txt",
                 doc_date=ago(102), amount=420, vendor="Quick Lube Irving",
                 extracted_metadata={"service_type": "Oil Change & Filter", "parts_cost": 120, "labor_cost": 300},
                 confidence_score=0.95),
            # Truck 85
            dict(id=str(uuid.uuid4()), truck_id="truck_85", doc_type=DocType.REGISTRATION,
                 filename="registration.txt", doc_date=ago(200), expiry_date=ago(200) + timedelta(365),
                 extracted_metadata={"doc_type": "registration"}, confidence_score=0.94),
            dict(id=str(uuid.uuid4()), truck_id="truck_85", driver_id="driver_002",
                 doc_type=DocType.MAINTENANCE, filename="maintenance_feb20.txt",
                 doc_date=ago(118), amount=650, vendor="Lone Star Diesel",
                 extracted_metadata={"service_type": "Transmission Service", "parts_cost": 350, "labor_cost": 300},
                 confidence_score=0.93),
            dict(id=str(uuid.uuid4()), truck_id="truck_85", driver_id="driver_002",
                 doc_type=DocType.FUEL_RECEIPT, filename="fuel_feb14.txt",
                 doc_date=ago(124), amount=510, vendor="Loves Travel Stop",
                 extracted_metadata={"gallons": 128.4, "price_per_gallon": 3.97}, confidence_score=0.97),
            # Truck 86
            dict(id=str(uuid.uuid4()), truck_id="truck_86", doc_type=DocType.REGISTRATION,
                 filename="registration.txt", doc_date=ago(370), expiry_date=ago(5),
                 extracted_metadata={"doc_type": "registration"}, confidence_score=0.94),
            dict(id=str(uuid.uuid4()), truck_id="truck_86", doc_type=DocType.INSPECTION,
                 filename="dot_inspection_2024.txt", doc_date=ago(290),
                 extracted_metadata={"doc_type": "inspection"}, confidence_score=0.92),
        ]

        for ds in doc_seeds:
            db.add(Document(**ds))

        db.flush()

        # --- Maintenance records (structured) ---
        maintenance_seeds = [
            dict(truck_id="truck_84", service_date=ago(155), service_type="Brake Pad Replacement",
                 vendor="Dallas Fleet Services", parts_cost=720, labor_cost=480, total_cost=1200,
                 odometer_at_service=298000, next_service_date=ago(155) + timedelta(365)),
            dict(truck_id="truck_84", service_date=ago(102), service_type="Oil Change & Filter",
                 vendor="Quick Lube Irving", parts_cost=120, labor_cost=300, total_cost=420,
                 odometer_at_service=306000, next_service_date=ago(102) + timedelta(90)),
            dict(truck_id="truck_85", service_date=ago(118), service_type="Transmission Service",
                 vendor="Lone Star Diesel", parts_cost=350, labor_cost=300, total_cost=650,
                 odometer_at_service=184000, next_service_date=ago(118) + timedelta(180)),
        ]
        for mr in maintenance_seeds:
            db.add(MaintenanceRecord(**mr))

        # --- Fuel records (structured) ---
        fuel_seeds = [
            dict(truck_id="truck_84", fill_date=ago(166), gallons=94.2, price_per_gallon=4.035,
                 total_cost=380.1, location="Pilot Travel Center - Irving TX", odometer=304000),
            dict(truck_id="truck_85", fill_date=ago(124), gallons=128.4, price_per_gallon=3.97,
                 total_cost=509.75, location="Loves Travel Stop - Dallas TX", odometer=193000),
        ]
        for fr in fuel_seeds:
            db.add(FuelRecord(**fr))

        print("Seed complete:")
        print(f"  {len(trucks_data)} trucks")
        print(f"  {len(drivers_data)} drivers")
        print(f"  {len(trailers_data)} trailers")
        print(f"  {len(doc_seeds)} documents")
        print(f"  {len(maintenance_seeds)} maintenance records")
        print(f"  {len(fuel_seeds)} fuel records")


if __name__ == "__main__":
    seed()
