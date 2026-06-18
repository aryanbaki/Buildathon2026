"""
Rule-based metadata extractor for synthetic fleet documents.
Use during bootstrap so we don't burn API calls on generated .txt files.
"""
import re
from datetime import date, datetime
from typing import List, Optional


def extract_synthetic_metadata(raw_text: str, filename: str = "") -> dict:
    """Parse known synthetic doc layouts into the standard metadata dict."""
    text = raw_text or ""
    lower = text.lower()
    name = (filename or "").lower()

    if "maintenance receipt" in lower or "maintenance_" in name:
        return _parse_maintenance(text)
    if "fuel receipt" in lower or name.startswith("fuel_"):
        return _parse_fuel(text)
    if "registration" in lower or "registration" in name:
        return _parse_registration(text)
    if "form 2290" in lower or "tax" in name:
        return _parse_tax_form(text)
    if "dot inspection" in lower or "inspection" in name:
        return _parse_inspection(text)
    if "insurance" in lower or "insurance" in name:
        return _parse_insurance(text)
    if "load manifest" in lower or "trip summary" in lower or "trip_" in name:
        return _parse_trip_summary(text)
    return {
        "doc_type": "other",
        "confidence": 0.5,
        "notes": "Unrecognized synthetic document format",
    }


def _parse_maintenance(text: str) -> dict:
    unit = _extract_unit_number(text)
    doc_date = _extract_date(text, labels=["Date:", "Service Date:"])
    parts = _money_after(text, r"Parts:\s*\$?([\d,]+\.?\d*)")
    labor = _money_after(text, r"Labor:\s*\$?([\d,]+\.?\d*)")
    total = _money_after(text, r"TOTAL:\s*\$?([\d,]+\.?\d*)")
    vendor = _line_after(text, "MAINTENANCE RECEIPT") or _first_nonempty_line(text)
    service = _line_after(text, "Service Performed:") or _between(text, "Service Performed:", "Parts:")
    return {
        "doc_type": "maintenance",
        "truck_unit_number": unit,
        "doc_date": doc_date,
        "amount": total or ((parts or 0) + (labor or 0) if parts or labor else None),
        "vendor": vendor.strip() if vendor else None,
        "service_type": service.strip() if service else None,
        "parts_cost": parts,
        "labor_cost": labor,
        "odometer": _extract_int(text, r"Odometer:\s*([\d,]+)"),
        "confidence": 0.95,
    }


def _parse_fuel(text: str) -> dict:
    return {
        "doc_type": "fuel_receipt",
        "truck_unit_number": _extract_unit_number(text),
        "doc_date": _extract_date(text, labels=["Date:"]),
        "amount": _money_after(text, r"TOTAL:\s*\$?([\d,]+\.?\d*)"),
        "vendor": _first_nonempty_line(text),
        "gallons": _money_after(text, r"Gallons:\s*([\d.]+)"),
        "price_per_gallon": _money_after(text, r"Price/Gal:\s*\$?([\d.]+)"),
        "odometer": _extract_int(text, r"Odometer:\s*([\d,]+)"),
        "confidence": 0.96,
    }


def _parse_registration(text: str) -> dict:
    return {
        "doc_type": "registration",
        "truck_unit_number": _extract_unit_number(text),
        "doc_date": _extract_date(text, labels=["Issue Date:"]),
        "expiry_date": _extract_date(text, labels=["Expiration Date:"]),
        "amount": _money_after(text, r"Annual Fee Paid:\s*\$?([\d,]+\.?\d*)"),
        "confidence": 0.94,
    }


def _parse_tax_form(text: str) -> dict:
    return {
        "doc_type": "tax_form",
        "truck_unit_number": _extract_unit_number(text),
        "doc_date": _extract_date(text, labels=["Payment Date:"]),
        "amount": _money_after(text, r"Tax Due:\s*\$?([\d,]+\.?\d*)"),
        "confidence": 0.97,
    }


def _parse_inspection(text: str) -> dict:
    return {
        "doc_type": "inspection",
        "truck_unit_number": _extract_unit_number(text),
        "doc_date": _extract_date(text, labels=["Inspection Date:", "Date:"]),
        "vendor": _line_after(text, "Inspector:"),
        "confidence": 0.92,
    }


def _parse_insurance(text: str) -> dict:
    return {
        "doc_type": "insurance",
        "truck_unit_number": _extract_unit_number(text),
        "doc_date": _extract_date(text, labels=["Effective Date:", "Policy Date:"]),
        "expiry_date": _extract_date(text, labels=["Expiration Date:", "Expires:"]),
        "amount": _money_after(text, r"Premium:\s*\$?([\d,]+\.?\d*)"),
        "confidence": 0.93,
    }


def _parse_trip_summary(text: str) -> dict:
    return {
        "doc_type": "other",
        "truck_unit_number": _extract_unit_number(text),
        "doc_date": _extract_date(text, labels=["Delivery Date:", "Trip Date:", "Date:"]),
        "amount": _money_after(text, r"(?:Linehaul|Revenue|TOTAL):\s*\$?([\d,]+\.?\d*)"),
        "vendor": _line_after(text, "Shipper:") or _line_after(text, "Broker:"),
        "confidence": 0.91,
        "notes": "trip revenue summary",
    }


def _extract_unit_number(text: str) -> Optional[int]:
    patterns = [
        r"Unit\s*#?\s*:?\s*(\d+)",
        r"TRK[_-]?0*(\d+)",
        r"Truck\s*#?\s*(\d+)",
        r"Unit Number:\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return int(match.group(1))
    return None


def _extract_date(text: str, labels: List[str]) -> Optional[str]:
    for label in labels:
        match = re.search(rf"{re.escape(label)}\s*([0-9/.\-A-Za-z ,]+)", text)
        if not match:
            continue
        raw = match.group(1).strip().split("\n")[0]
        for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%B %d, %Y", "%B %d %Y"):
            try:
                return datetime.strptime(raw, fmt).date().isoformat()
            except ValueError:
                continue
    return None


def _money_after(text: str, pattern: str) -> Optional[float]:
    match = re.search(pattern, text, re.I)
    if not match:
        return None
    try:
        return round(float(match.group(1).replace(",", "")), 2)
    except ValueError:
        return None


def _extract_int(text: str, pattern: str) -> Optional[int]:
    match = re.search(pattern, text, re.I)
    if not match:
        return None
    try:
        return int(match.group(1).replace(",", ""))
    except ValueError:
        return None


def _line_after(text: str, label: str) -> Optional[str]:
    match = re.search(rf"{re.escape(label)}\s*(.+)", text)
    return match.group(1).strip() if match else None


def _between(text: str, start: str, end: str) -> Optional[str]:
    match = re.search(rf"{re.escape(start)}\s*(.+?)\s*{re.escape(end)}", text, re.S)
    return match.group(1).strip() if match else None


def _first_nonempty_line(text: str) -> Optional[str]:
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned and not cleaned.startswith("="):
            return cleaned
    return None
