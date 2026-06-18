"""
Charan — metadata_extractor.py
Uses Claude Haiku to extract structured metadata from raw document text.
Returns a typed dict that maps to the Document model.
"""
import json
import re
from datetime import date
from typing import Optional

import anthropic

from backend.config import get_settings

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

EXTRACTION_PROMPT = """You are a fleet document parser for a trucking company.
Extract structured metadata from the document text below.

Return ONLY a valid JSON object with these exact keys:
{
  "doc_type": one of [title, registration, insurance, maintenance, fuel_receipt, tax_form, inspection, repair_invoice, other],
  "truck_unit_number": integer or null,
  "driver_name": string or null,
  "trailer_unit_number": integer or null,
  "doc_date": "YYYY-MM-DD" or null,
  "expiry_date": "YYYY-MM-DD" or null,
  "amount": float or null (total dollar amount if present),
  "vendor": string or null (company/shop name),
  "service_type": string or null (what was done, for maintenance),
  "parts_cost": float or null,
  "labor_cost": float or null,
  "gallons": float or null (for fuel receipts),
  "price_per_gallon": float or null,
  "odometer": integer or null,
  "confidence": float between 0 and 1,
  "notes": string or null (anything unusual or ambiguous)
}

Rules:
- Use null for any field you cannot confidently extract.
- confidence: 0.9+ = clearly stated, 0.7-0.9 = inferred, <0.7 = uncertain.
- For amounts, use the TOTAL (after tax) if present, else subtotal.
- truck_unit_number: look for "Unit #", "Unit:", "Truck #", or similar labels.
- Do NOT invent data. If uncertain, use null and lower the confidence.

Document text:
\"\"\"
{text}
\"\"\"

Return ONLY the JSON object, no explanation."""


def extract_metadata(raw_text: str) -> dict:
    """
    Run Claude Haiku extraction on raw document text.
    Returns structured metadata dict.
    """
    try:
        message = client.messages.create(
            model=settings.extraction_model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": EXTRACTION_PROMPT.format(text=raw_text[:6000]),
            }],
        )
        content = message.content[0].text.strip()

        # Strip markdown fences if model adds them
        content = re.sub(r"^```json\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        metadata = json.loads(content)
        return _validate_and_clean(metadata)

    except (json.JSONDecodeError, IndexError, anthropic.APIError) as e:
        return {
            "doc_type": "other",
            "confidence": 0.0,
            "notes": f"Extraction failed: {str(e)}",
        }


def _validate_and_clean(meta: dict) -> dict:
    """Validate types and clamp ranges."""
    # Clamp confidence
    if "confidence" in meta:
        meta["confidence"] = max(0.0, min(1.0, float(meta["confidence"] or 0)))

    # Parse dates
    for field in ("doc_date", "expiry_date"):
        if meta.get(field):
            try:
                date.fromisoformat(meta[field])
            except ValueError:
                meta[field] = None

    # Ensure numeric fields are correct types
    for field in ("amount", "parts_cost", "labor_cost", "gallons", "price_per_gallon"):
        if meta.get(field) is not None:
            try:
                meta[field] = round(float(meta[field]), 2)
            except (ValueError, TypeError):
                meta[field] = None

    if meta.get("odometer") is not None:
        try:
            meta["odometer"] = int(meta["odometer"])
        except (ValueError, TypeError):
            meta["odometer"] = None

    if meta.get("truck_unit_number") is not None:
        try:
            meta["truck_unit_number"] = int(meta["truck_unit_number"])
        except (ValueError, TypeError):
            meta["truck_unit_number"] = None

    return meta


def batch_extract(texts: list[str]) -> list[dict]:
    """Extract metadata from multiple documents."""
    return [extract_metadata(t) for t in texts]
