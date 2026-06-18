"""
Generates realistic messy synthetic fleet documents as text files
(stand-ins for PDFs/receipts). Run before seeding the database.

Usage: python generate_documents.py
Output: ../../data/raw_documents/truck_XX/
"""
import os
import random
from datetime import date, timedelta
from faker import Faker

fake = Faker()
random.seed(42)

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../data/raw_documents")

TRUCKS = [
    {"id": "truck_84", "unit": 84, "make": "Freightliner", "model": "Cascadia", "year": 2019, "vin": "1FUJGEBG0JLGE1234"},
    {"id": "truck_85", "unit": 85, "make": "Kenworth", "model": "T680", "year": 2020, "vin": "1XKYDP9X4LJ123456"},
    {"id": "truck_86", "unit": 86, "make": "Peterbilt", "model": "579", "year": 2018, "vin": "1XPBD49X4JD123789"},
]

VENDORS = ["Dallas Fleet Services", "Quick Lube Irving", "Lone Star Diesel", "TX Tire Pros", "DFW Parts Warehouse"]

SERVICE_TYPES = [
    ("Oil Change & Filter", 280, 420),
    ("Brake Pad Replacement", 900, 1400),
    ("Tire Rotation", 120, 200),
    ("Engine Diagnostic", 150, 350),
    ("Transmission Service", 400, 800),
    ("AC Repair", 300, 600),
    ("DOT Inspection", 80, 150),
    ("Battery Replacement", 200, 380),
]


def rand_date(start_days_ago=180, end_days_ago=0):
    offset = random.randint(end_days_ago, start_days_ago)
    return date.today() - timedelta(days=offset)


def make_maintenance_receipt(truck, service_type, vendor, service_date, parts, labor):
    total = parts + labor
    return f"""
MAINTENANCE RECEIPT
===================
{vendor}
{fake.address()}
Tel: {fake.phone_number()}

Date: {service_date.strftime('%m/%d/%Y')}
Work Order: WO-{random.randint(10000,99999)}

Vehicle Information:
  Unit #: {truck['unit']}
  VIN: {truck['vin']}
  Make/Model: {truck['year']} {truck['make']} {truck['model']}
  Odometer: {random.randint(120000, 450000)} miles

Service Performed:
  {service_type}

Parts:   ${parts:.2f}
Labor:   ${labor:.2f}
Tax:     ${total * 0.0825:.2f}
TOTAL:   ${total * 1.0825:.2f}

Technician: {fake.name()}
Authorized by: {fake.name()}

Next service due: {(service_date + timedelta(days=random.choice([90, 180, 365]))).strftime('%m/%d/%Y')}
""".strip()


def make_fuel_receipt(truck, fill_date, gallons, ppg, location):
    total = gallons * ppg
    return f"""
FUEL RECEIPT
============
{location}
{fake.address()}

Date: {fill_date.strftime('%m/%d/%Y')}  Time: {random.randint(6,22):02d}:{random.choice(['00','15','30','45'])}
Transaction #: {random.randint(100000,999999)}

Unit: {truck['unit']}
VIN: {truck['vin']}
Driver: {fake.name()}
Odometer: {random.randint(100000,500000)}

Diesel Fuel
Gallons: {gallons:.3f}
Price/Gal: ${ppg:.3f}
TOTAL: ${total:.2f}

Payment: Fleet Card ****{random.randint(1000,9999)}
""".strip()


def make_registration(truck, issue_date):
    expiry = issue_date + timedelta(days=365)
    return f"""
STATE OF TEXAS
MOTOR VEHICLE REGISTRATION

Registration Number: TX-{random.randint(100000,999999)}
Issue Date: {issue_date.strftime('%m/%d/%Y')}
Expiration Date: {expiry.strftime('%m/%d/%Y')}

Vehicle Information:
  Year: {truck['year']}
  Make: {truck['make']}
  Model: {truck['model']}
  VIN: {truck['vin']}
  License Plate: {fake.license_plate()}

Registered Owner: {fake.company()} Trucking LLC
Address: {fake.address()}

Annual Fee Paid: $847.00
Weight Class: Class 8 (80,000 lbs GVW)

This registration must be kept in the vehicle at all times.
""".strip()


def make_tax_form(truck, year):
    return f"""
IRS FORM 2290 - HEAVY HIGHWAY VEHICLE USE TAX
Tax Year: {year}

Taxpayer: {fake.company()} Trucking LLC
EIN: {random.randint(10,99)}-{random.randint(1000000,9999999)}

Vehicle VIN: {truck['vin']}
Unit Number: {truck['unit']}
Taxable Gross Weight: 80,000 lbs
Category: W (75,001 lbs and over)

Tax Due: $550.00
Payment Date: {date(year, 8, 31).strftime('%m/%d/%Y')}
Filing Period: July 1, {year} - June 30, {year+1}

Stamped by IRS: RECEIVED {date(year, 9, random.randint(1,15)).strftime('%m/%d/%Y')}
""".strip()


def generate_for_truck(truck):
    out_dir = os.path.join(BASE_DIR, truck["id"])
    os.makedirs(out_dir, exist_ok=True)

    files = []

    # 1 registration
    reg_date = rand_date(400, 200)
    reg_content = make_registration(truck, reg_date)
    reg_path = os.path.join(out_dir, "registration.txt")
    with open(reg_path, "w") as f:
        f.write(reg_content)
    files.append(reg_path)

    # 1 tax form
    tax_content = make_tax_form(truck, 2025)
    tax_path = os.path.join(out_dir, "form_2290_2025.txt")
    with open(tax_path, "w") as f:
        f.write(tax_content)
    files.append(tax_path)

    # 4-6 maintenance receipts
    for i in range(random.randint(4, 6)):
        stype, pmin, pmax = random.choice(SERVICE_TYPES)
        parts = round(random.uniform(pmin * 0.4, pmax * 0.4), 2)
        labor = round(random.uniform(pmin * 0.6, pmax * 0.6), 2)
        vendor = random.choice(VENDORS)
        sdate = rand_date(180, 5)
        content = make_maintenance_receipt(truck, stype, vendor, sdate, parts, labor)
        fname = f"maintenance_{sdate.strftime('%b%d').lower()}.txt"
        path = os.path.join(out_dir, fname)
        with open(path, "w") as f:
            f.write(content)
        files.append(path)

    # 3-5 fuel receipts
    for i in range(random.randint(3, 5)):
        gallons = round(random.uniform(80, 200), 3)
        ppg = round(random.uniform(3.45, 4.20), 3)
        location = f"{random.choice(['Pilot', 'Loves', 'Flying J', 'TA'])} Travel Center"
        fdate = rand_date(90, 1)
        content = make_fuel_receipt(truck, fdate, gallons, ppg, location)
        fname = f"fuel_{fdate.strftime('%b%d').lower()}_{i+1}.txt"
        path = os.path.join(out_dir, fname)
        with open(path, "w") as f:
            f.write(content)
        files.append(path)

    return files


if __name__ == "__main__":
    all_files = []
    for truck in TRUCKS:
        files = generate_for_truck(truck)
        all_files.extend(files)
        print(f"Truck {truck['unit']}: {len(files)} documents generated")

    print(f"\nTotal: {len(all_files)} documents in {BASE_DIR}")
