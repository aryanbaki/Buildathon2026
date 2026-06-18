"""
Charan - run_ingest_demo.py
Smoke demo for the database ingestion pipeline.

Run from the repo root:
    python -m backend.ingestion.run_ingest_demo

This uses an in-memory SQLite database and a mock metadata extractor so it can
run without PostgreSQL, ChromaDB, Tesseract, or an Anthropic API key.
"""
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.models import Base, Document, Driver, MaintenanceRecord, Trailer, Truck
from backend.ingestion.pipeline import ingest_loaded_document


MESSY_MAINTENANCE_TEXT = """
DALLAS FLEET SERVICES                     Invoice # DFS-88421
   1038 Loop 12, Irving, TX

DATE: 2026-05-18       UNIT: 84        DRIVER: Carlos Mendez
TRAILER: 101           ODOMETER: 312450

Work performed:
- Brake pad replacement, axle 2
- Shop supplies / disposal fee

PARTS: $720.00
LABOR: $480.00
TAX:   $0.00
TOTAL DUE: $1,200.00

Paid by card ending 4412. Signature smudged.
"""


def main() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        seed_minimal_fleet(db)

        loaded = {
            "filename": "truck_84_brake_invoice_messy.txt",
            "file_path": "demo://truck_84_brake_invoice_messy.txt",
            "raw_text": MESSY_MAINTENANCE_TEXT,
            "file_type": "txt",
            "size_bytes": len(MESSY_MAINTENANCE_TEXT.encode("utf-8")),
            "error": None,
        }

        document = ingest_loaded_document(
            loaded,
            db,
            metadata_extractor=mock_extract_metadata,
        )
        db.commit()

        maintenance = db.query(MaintenanceRecord).filter_by(document_id=document.id).one()
        saved_document = db.query(Document).filter_by(id=document.id).one()

        print("Charan ingestion demo complete")
        print(f"Document ID: {saved_document.id}")
        print(f"Truck link: {saved_document.truck_id}")
        print(f"Driver link: {saved_document.driver_id}")
        print(f"Trailer link: {saved_document.trailer_id}")
        print(f"Doc type: {saved_document.doc_type.value}")
        print(f"Vendor: {saved_document.vendor}")
        print(f"Amount: ${saved_document.amount:,.2f}")
        print(f"Structured maintenance row: {maintenance.service_type}")
        print(f"Parts: ${maintenance.parts_cost:,.2f}")
        print(f"Labor: ${maintenance.labor_cost:,.2f}")


def seed_minimal_fleet(db) -> None:
    db.add_all([
        Truck(
            id="truck_84",
            unit_number=84,
            vin="1FUJGEBG0JLGE1234",
            make="Freightliner",
            model="Cascadia",
            year=2019,
            license_plate="TX-84FLT",
            state="TX",
            status="active",
            purchase_date=date(2019, 3, 15),
            purchase_price=145000,
            odometer=312000,
        ),
        Driver(
            id="driver_001",
            name="Carlos Mendez",
            cdl_number="TX-CDL-7734221",
            cdl_expiry=date(2027, 6, 30),
            status="active",
        ),
        Trailer(
            id="trailer_01",
            unit_number=101,
            trailer_type="Dry Van",
            license_plate="TX-T101",
            state="TX",
            status="active",
        ),
    ])
    db.commit()


def mock_extract_metadata(raw_text: str) -> dict:
    return {
        "doc_type": "maintenance",
        "truck_unit_number": 84,
        "driver_name": "Carlos Mendez",
        "trailer_unit_number": 101,
        "doc_date": "2026-05-18",
        "expiry_date": None,
        "amount": 1200.00,
        "vendor": "Dallas Fleet Services",
        "service_type": "Brake Pad Replacement",
        "parts_cost": 720.00,
        "labor_cost": 480.00,
        "gallons": None,
        "price_per_gallon": None,
        "odometer": 312450,
        "confidence": 0.97,
        "notes": "Synthetic messy maintenance invoice for pipeline smoke test.",
    }


if __name__ == "__main__":
    main()
