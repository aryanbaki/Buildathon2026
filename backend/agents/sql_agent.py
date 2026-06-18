"""
Teja — sql_agent.py
Generates and executes SQL from natural language using Claude Sonnet.
Only runs SELECT queries — never mutates data.
"""
import re
import json
import anthropic
from sqlalchemy import text
from backend.config import get_settings
from backend.database.db import get_db

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

SCHEMA = """
Tables:
- trucks(id, unit_number, make, model, year, license_plate, state, status, purchase_date, purchase_price, odometer)
- drivers(id, name, cdl_number, cdl_expiry, phone, email, hire_date, status)
- documents(id, truck_id, driver_id, doc_type, filename, doc_date, expiry_date, amount, vendor, confidence_score)
- maintenance_records(id, truck_id, service_date, service_type, vendor, parts_cost, labor_cost, total_cost, odometer_at_service, next_service_date)
- fuel_records(id, truck_id, fill_date, gallons, price_per_gallon, total_cost, location, odometer)
- driver_assignments(id, truck_id, driver_id, start_date, end_date, is_primary)

doc_type values: title, registration, insurance, maintenance, fuel_receipt, tax_form, inspection, repair_invoice, other
truck status values: active, inactive, sold

Rules:
- ALWAYS use parameterized queries. Return only SELECT statements.
- Use truck_id like 'truck_84' (string). unit_number is the integer (84).
- For "last month" use: EXTRACT(MONTH FROM date_col) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month')
- For "expiring soon" use: expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
- Always JOIN trucks ON trucks.id = <table>.truck_id when showing truck info.
"""

SQL_PROMPT = f"""You are a PostgreSQL expert for a fleet management system.
{SCHEMA}

Given the question, return ONLY a JSON object:
{{"sql": "SELECT ...", "explanation": "one sentence"}}

Never use DROP, DELETE, UPDATE, INSERT, or any DDL.
Question: {{question}}
Truck filter (if any): {{truck_id}}"""


def run(question: str, truck_id: str = None) -> dict:
    try:
        msg = client.messages.create(
            model=settings.routing_model,
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": SQL_PROMPT.format(question=question, truck_id=truck_id or "none"),
            }],
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        parsed = json.loads(raw)
        sql = parsed.get("sql", "")
    except Exception as e:
        return _error_response(f"SQL generation failed: {e}")

    # Safety: block any mutating keywords
    if re.search(r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|CREATE)\b", sql, re.IGNORECASE):
        return _error_response("Unsafe query blocked.")

    try:
        with get_db() as db:
            result = db.execute(text(sql))
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    except Exception as e:
        return _error_response(f"SQL execution failed: {e}")

    from backend.rag.answer_generator import generate_sql_answer
    answer = generate_sql_answer(question, sql, rows)

    return {
        "answer": answer,
        "query_type": "sql",
        "sql_query": sql,
        "sources": [],
        "raw_rows": rows[:20],
    }


def _error_response(msg: str) -> dict:
    return {"answer": msg, "query_type": "sql", "sql_query": None, "sources": []}
