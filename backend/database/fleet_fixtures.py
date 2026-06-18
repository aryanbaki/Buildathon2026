"""Shared fleet entity fixtures for seeding and synthetic document generation."""
from datetime import date

TRUCKS = [
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
    dict(id="truck_87", unit_number=87, vin="1FUJGLDR5KLHZ4321",
         make="Freightliner", model="Columbia", year=2017,
         license_plate="TX-87FLT", state="TX", status="active",
         purchase_date=date(2017, 5, 10), purchase_price=98000, odometer=521000),
    dict(id="truck_88", unit_number=88, vin="1NKWL49X8LJ654321",
         make="Kenworth", model="W900", year=2021,
         license_plate="TX-88FLT", state="TX", status="active",
         purchase_date=date(2021, 2, 14), purchase_price=175000, odometer=156000),
    dict(id="truck_89", unit_number=89, vin="1XPWD49X2MD987654",
         make="Peterbilt", model="389", year=2022,
         license_plate="TX-89FLT", state="TX", status="active",
         purchase_date=date(2022, 9, 1), purchase_price=189000, odometer=89000),
    dict(id="truck_90", unit_number=90, vin="1FUJGBDV8CLAA1111",
         make="Freightliner", model="M2", year=2016,
         license_plate="TX-90FLT", state="TX", status="active",
         purchase_date=date(2016, 8, 20), purchase_price=72000, odometer=398000),
    dict(id="truck_91", unit_number=91, vin="1XKWDB0X8LJ222222",
         make="Kenworth", model="T880", year=2019,
         license_plate="TX-91FLT", state="TX", status="active",
         purchase_date=date(2019, 11, 5), purchase_price=168000, odometer=267000),
    dict(id="truck_92", unit_number=92, vin="1XPBDP9X8KD333333",
         make="Peterbilt", model="567", year=2018,
         license_plate="TX-92FLT", state="TX", status="inactive",
         purchase_date=date(2018, 4, 12), purchase_price=142000, odometer=445000),
    dict(id="truck_93", unit_number=93, vin="1FUJGLDR1KLBB4444",
         make="Freightliner", model="Cascadia", year=2023,
         license_plate="TX-93FLT", state="TX", status="active",
         purchase_date=date(2023, 1, 18), purchase_price=198000, odometer=42000),
]

DRIVERS = [
    dict(id="driver_001", name="Carlos Mendez", cdl_number="TX-CDL-7734221",
         cdl_expiry=date(2027, 6, 30), phone="214-555-0101",
         email="cmendez@fleet.com", hire_date=date(2020, 2, 1), status="active"),
    dict(id="driver_002", name="James Whitfield", cdl_number="TX-CDL-8821045",
         cdl_expiry=date(2026, 9, 15), phone="972-555-0188",
         email="jwhitfield@fleet.com", hire_date=date(2019, 8, 15), status="active"),
    dict(id="driver_003", name="Maria Santos", cdl_number="TX-CDL-9934512",
         cdl_expiry=date(2025, 12, 31), phone="469-555-0234",
         email="msantos@fleet.com", hire_date=date(2021, 5, 10), status="active"),
    dict(id="driver_004", name="Robert Chen", cdl_number="TX-CDL-1102934",
         cdl_expiry=date(2028, 3, 20), phone="817-555-0445",
         email="rchen@fleet.com", hire_date=date(2018, 6, 1), status="active"),
    dict(id="driver_005", name="Angela Brooks", cdl_number="TX-CDL-2203847",
         cdl_expiry=date(2027, 11, 8), phone="903-555-0556",
         email="abrooks@fleet.com", hire_date=date(2022, 4, 18), status="active"),
]

TRAILERS = [
    dict(id="trailer_01", unit_number=101, trailer_type="Dry Van",
         capacity_tons=22.0, license_plate="TX-T101", state="TX", status="active"),
    dict(id="trailer_02", unit_number=102, trailer_type="Reefer",
         capacity_tons=20.0, license_plate="TX-T102", state="TX", status="active"),
    dict(id="trailer_03", unit_number=103, trailer_type="Flatbed",
         capacity_tons=24.0, license_plate="TX-T103", state="TX", status="active"),
    dict(id="trailer_04", unit_number=104, trailer_type="Dry Van",
         capacity_tons=22.0, license_plate="TX-T104", state="TX", status="active"),
]

# Slim records for the synthetic document generator
SYNTHETIC_TRUCKS = [
    {
        "id": t["id"],
        "unit": t["unit_number"],
        "make": t["make"],
        "model": t["model"],
        "year": t["year"],
        "vin": t["vin"],
    }
    for t in TRUCKS
]
