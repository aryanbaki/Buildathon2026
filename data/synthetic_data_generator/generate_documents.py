"""
Generates realistic messy synthetic fleet documents as text files.
Run before bootstrap_fleet_data.

Usage (from repo root):
    python data/synthetic_data_generator/generate_documents.py

Output: data/raw_documents/truck_XX/
"""
import os
import random
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from backend.database.fleet_fixtures import SYNTHETIC_TRUCKS, TRAILERS, DRIVERS

random.seed(42)

BASE_DIR = REPO_ROOT / "data" / "raw_documents"

VENDORS = [
    "Dallas Fleet Services", "Quick Lube Irving", "Lone Star Diesel",
    "TX Tire Pros", "DFW Parts Warehouse", "Irving Truck Center",
]

SERVICE_TYPES = [
    ("Oil Change & Filter", 280, 420),
    ("Brake Pad Replacement", 900, 1400),
    ("Tire Rotation", 120, 200),
    ("Engine Diagnostic", 150, 350),
    ("Transmission Service", 400, 800),
    ("AC Repair", 300, 600),
    ("DOT Inspection", 80, 150),
    ("Battery Replacement", 200, 380),
    ("DEF System Repair", 250, 500),
    ("Coolant Flush", 90, 180),
]

STREETS = ["Main St", "Commerce St", "Mockingbird Ln", "Loop 12", "Industrial Blvd"]
COMPANIES = [
    "Bluebonnet Foods", "Trinity Freight", "North Texas Steel",
    "Metroplex Produce", "Red River Logistics", "Lone Star Supply",
]
FIRST_NAMES = ["Carlos", "James", "Maria", "Robert", "Angela", "Derrick", "Nina", "Omar"]
LAST_NAMES = ["Mendez", "Whitfield", "Santos", "Chen", "Brooks", "Patel", "Garcia", "Reed"]

UNIT_LABEL_STYLES = [
    lambda u: f"Unit #: {u}",
    lambda u: f"Unit Number: {u}",
    lambda u: f"TRK-{u:03d}",
    lambda u: f"Truck {u}",
    lambda u: f"TRK_{u}",
]


def rand_date(start_days_ago=180, end_days_ago=0):
    return date.today() - timedelta(days=random.randint(end_days_ago, start_days_ago))


def fake_address() -> str:
    return f"{random.randint(100, 9999)} {random.choice(STREETS)}, Dallas, TX {random.randint(75001, 75399)}"


def fake_phone() -> str:
    return f"{random.choice(['214', '469', '972', '817'])}-555-{random.randint(1000, 9999)}"


def fake_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def fake_company() -> str:
    return random.choice(COMPANIES)


def fake_license_plate() -> str:
    return f"TX-{random.choice(['FLT', 'TRK', 'HVY'])}{random.randint(100, 999)}"


def unit_label(unit: int) -> str:
    return random.choice(UNIT_LABEL_STYLES)(unit)


def maybe_ocr_noise(text: str, probability: float = 0.15) -> str:
    """Introduce light OCR-style character swaps on ~15% of docs."""
    if random.random() > probability:
        return text
    swaps = {"0": "O", "O": "0", "1": "I", "I": "1", "5": "S"}
    chars = list(text)
    for i, ch in enumerate(chars):
        if ch in swaps and random.random() < 0.02:
            chars[i] = swaps[ch]
    return "".join(chars)


def format_date(d: Optional[date]) -> str:
    if d is None:
        return "___________"
    style = random.choice(["mdy", "long", "iso"])
    if style == "mdy":
        return d.strftime("%m/%d/%Y")
    if style == "long":
        return d.strftime("%B %d, %Y")
    return d.isoformat()


def make_maintenance_receipt(truck, service_type, vendor, service_date, parts, labor):
    total = parts + labor
    label = unit_label(truck["unit"])
    return f"""
MAINTENANCE RECEIPT
===================
{vendor}
{fake_address()}
Tel: {fake_phone()}

Date: {format_date(service_date)}
Work Order: WO-{random.randint(10000, 99999)}

Vehicle Information:
  {label}
  VIN: {truck['vin']}
  Make/Model: {truck['year']} {truck['make']} {truck['model']}
  Odometer: {random.randint(120000, 450000)} miles

Service Performed:
  {service_type}

Parts:   ${parts:.2f}
Labor:   ${labor:.2f}
Tax:     ${total * 0.0825:.2f}
TOTAL:   ${total * 1.0825:.2f}

Technician: {fake_name()}
Authorized by: {fake_name()}

Next service due: {format_date(service_date + timedelta(days=random.choice([90, 180, 365])))}
""".strip()


def make_multi_maintenance_history(truck):
    """One multi-entry maintenance history document."""
    label = unit_label(truck["unit"])
    entries = []
    for _ in range(random.randint(3, 4)):
        stype, pmin, pmax = random.choice(SERVICE_TYPES[:6])
        parts = round(random.uniform(pmin * 0.4, pmax * 0.4), 2)
        labor = round(random.uniform(pmin * 0.6, pmax * 0.6), 2)
        sdate = rand_date(365, 30)
        entries.append(
            f"- {format_date(sdate)} | {stype} | Parts ${parts:.2f} | Labor ${labor:.2f} | "
            f"Total ${(parts + labor) * 1.0825:.2f} | {random.choice(VENDORS)}"
        )
    return f"""
FLEET MAINTENANCE HISTORY — {label}
VIN: {truck['vin']}
{truck['year']} {truck['make']} {truck['model']}

Service log:
{chr(10).join(entries)}

Shop notes: Driver reported intermittent check-engine light on last two entries.
""".strip()


def make_fuel_receipt(truck, fill_date, gallons, ppg, location):
    total = gallons * ppg
    label = unit_label(truck["unit"])
    return f"""
FUEL RECEIPT
============
{location}
{fake_address()}

Date: {format_date(fill_date)}  Time: {random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}
Transaction #: {random.randint(100000, 999999)}

{label}
VIN: {truck['vin']}
Driver: {random.choice(DRIVERS)['name']}
Odometer: {random.randint(100000, 500000)}

Diesel Fuel
Gallons: {gallons:.3f}
Price/Gal: ${ppg:.3f}
TOTAL: ${total:.2f}

Payment: Fleet Card ****{random.randint(1000, 9999)}
""".strip()


def make_registration(truck, issue_date):
    expiry = issue_date + timedelta(days=365)
    return f"""
STATE OF TEXAS
MOTOR VEHICLE REGISTRATION

Registration Number: TX-{random.randint(100000, 999999)}
Issue Date: {format_date(issue_date)}
Expiration Date: {format_date(expiry)}

Vehicle Information:
  Year: {truck['year']}
  Make: {truck['make']}
  Model: {truck['model']}
  VIN: {truck['vin']}
  License Plate: {fake_license_plate()}

Registered Owner: {fake_company()} Trucking LLC
Address: {fake_address()}

Annual Fee Paid: $847.00
Weight Class: Class 8 (80,000 lbs GVW)

This registration must be kept in the vehicle at all times.
""".strip()


def make_tax_form(truck, year):
    return f"""
IRS FORM 2290 - HEAVY HIGHWAY VEHICLE USE TAX
Tax Year: {year}

Taxpayer: {fake_company()} Trucking LLC
EIN: {random.randint(10, 99)}-{random.randint(1000000, 9999999)}

Vehicle VIN: {truck['vin']}
Unit Number: {truck['unit']}
Taxable Gross Weight: 80,000 lbs
Category: W (75,001 lbs and over)

Tax Due: $550.00
Payment Date: {format_date(date(year, 8, 31))}
Filing Period: July 1, {year} - June 30, {year + 1}

Stamped by IRS: RECEIVED {format_date(date(year, 9, random.randint(1, 15)))}
""".strip()


def make_inspection(truck, inspection_date):
    label = unit_label(truck["unit"])
    return f"""
DOT ANNUAL INSPECTION REPORT
============================
Inspection Date: {format_date(inspection_date)}
Inspector: {fake_name()}  Cert #: TX-DOT-{random.randint(10000, 99999)}

{label}
VIN: {truck['vin']}
Result: PASS with minor notes

Brakes: OK   Tires: OK   Lights: OK   Coupling: OK
Notes: Minor air leak repaired at gladhand. Cleared for operation.
""".strip()


def make_insurance(truck, effective_date):
    expiry = effective_date + timedelta(days=365)
    label = unit_label(truck["unit"])
    return f"""
COMMERCIAL AUTO INSURANCE CERTIFICATE
Carrier: Lone Star Mutual Insurance
Policy Number: LSM-CA-{random.randint(100000, 999999)}

Effective Date: {format_date(effective_date)}
Expiration Date: {format_date(expiry)}

Covered Unit: {label}
VIN: {truck['vin']}
Premium: ${random.randint(4200, 8900)}.00 annual
""".strip()


def make_trip_summary(truck, trip_date, revenue):
    trailer = random.choice(TRAILERS)
    label = unit_label(truck["unit"])
    return f"""
LOAD MANIFEST / TRIP SUMMARY
============================
Trip Date: {format_date(trip_date)}
{label}
Trailer: T-{trailer['unit_number']}
Driver: {random.choice(DRIVERS)['name']}

Route: Dallas TX -> Houston TX -> Dallas TX
Shipper: {fake_company()}
Broker: {fake_company()} Logistics

Linehaul Revenue: ${revenue:,.2f}
Fuel surcharge: ${round(revenue * 0.08, 2):,.2f}
TOTAL: ${round(revenue * 1.08, 2):,.2f}
""".strip()


def write_file(path: Path, content: str, noisy: bool = True):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = maybe_ocr_noise(content) if noisy else content
    path.write_text(text, encoding="utf-8")


def generate_for_truck(truck):
    out_dir = BASE_DIR / truck["id"]
    files = []

    reg_date = rand_date(400, 200)
    write_file(out_dir / "registration.txt", make_registration(truck, reg_date))
    files.append(out_dir / "registration.txt")

    write_file(out_dir / "form_2290_2025.txt", make_tax_form(truck, 2025))
    files.append(out_dir / "form_2290_2025.txt")

    if random.random() < 0.6:
        idate = rand_date(300, 60)
        write_file(out_dir / f"inspection_{idate.strftime('%Y')}.txt", make_inspection(truck, idate))
        files.append(out_dir / f"inspection_{idate.strftime('%Y')}.txt")

    if random.random() < 0.5:
        edate = rand_date(350, 120)
        write_file(out_dir / "insurance_cert.txt", make_insurance(truck, edate))
        files.append(out_dir / "insurance_cert.txt")

    for i in range(random.randint(4, 6)):
        stype, pmin, pmax = random.choice(SERVICE_TYPES)
        parts = round(random.uniform(pmin * 0.4, pmax * 0.4), 2)
        labor = round(random.uniform(pmin * 0.6, pmax * 0.6), 2)
        sdate = rand_date(180, 5)
        content = make_maintenance_receipt(truck, stype, random.choice(VENDORS), sdate, parts, labor)
        path = out_dir / f"maintenance_{sdate.strftime('%b%d').lower()}_{i}.txt"
        write_file(path, content)
        files.append(path)

    for i in range(random.randint(3, 5)):
        gallons = round(random.uniform(80, 200), 3)
        ppg = round(random.uniform(3.45, 4.20), 3)
        location = f"{random.choice(['Pilot', 'Loves', 'Flying J', 'TA'])} Travel Center"
        fdate = rand_date(90, 1)
        path = out_dir / f"fuel_{fdate.strftime('%b%d').lower()}_{i}.txt"
        write_file(path, make_fuel_receipt(truck, fdate, gallons, ppg, location))
        files.append(path)

    for i in range(random.randint(1, 2)):
        tdate = rand_date(120, 10)
        revenue = round(random.uniform(1800, 6200), 2)
        path = out_dir / f"trip_{tdate.strftime('%b%d').lower()}_{i}.txt"
        write_file(path, make_trip_summary(truck, tdate, revenue))
        files.append(path)

    if truck["unit"] == 84:
        write_file(out_dir / "maintenance_history_multipage.txt", make_multi_maintenance_history(truck))
        files.append(out_dir / "maintenance_history_multipage.txt")
        # intentional missing date field
        broken = make_fuel_receipt(truck, None, 110.5, 3.89, "Pilot Travel Center")
        write_file(out_dir / "fuel_missing_date.txt", broken, noisy=False)
        files.append(out_dir / "fuel_missing_date.txt")

    return files


if __name__ == "__main__":
    all_files = []
    for truck in SYNTHETIC_TRUCKS:
        files = generate_for_truck(truck)
        all_files.extend(files)
        print(f"Truck {truck['unit']}: {len(files)} documents generated")

    print(f"\nTotal: {len(all_files)} documents in {BASE_DIR}")
