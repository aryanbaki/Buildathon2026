# Fleet Document Intelligence — Known Gaps & Fix Tracker

This file tracks architectural gaps identified against Statement 7 requirements.  
Each gap has a severity, owner, and concrete fix. Close these before demo.

---

## Gap 1 — Trailer entity missing from linking pipeline
**Severity:** 🔴 Critical (direct miss against spec)  
**Owner:** Charan (entity_linker.py) + Teja (schemas.py)  

**Problem:**  
Statement 7 explicitly requires linking each document to the correct **truck, driver, and trailer**.  
`entity_linker.py` currently extracts truck_id and driver_id only. Trailer is absent everywhere —  
entity linker, DB schema, API response, and the retriever interface.

**Fix:**  
- Add `trailer_id` field to `ingestion/entity_linker.py` extraction prompt  
- Add `trailer_id` column to `database/models.py` (Document table)  
- Add `trailer_id` filter to `rag/retriever.py` query signature  
- Add `trailer_id` to `POST /ask` request schema and source objects in response  
- Add 2–3 demo queries that reference trailers (e.g. "Show me all docs for trailer T-22")

---

## Gap 2 — Graph module undocumented and missing from architecture diagram
**Severity:** 🟠 High (confuses judges, looks like dead weight)  
**Owner:** Aryan (graph/) + Teja (arch diagram in README)  

**Problem:**  
`graph/graph_builder.py`, `graph_queries.py`, and `graph_schema.py` exist in the file tree  
but do not appear in the architecture diagram and are never explained in the README.  
Judges will either think it's unfinished or wonder why it's there.

**Decision needed (pick one):**  
- **Option A — Keep and justify:** Add graph layer to arch diagram. One-line description:  
  *"Knowledge graph linking trucks ↔ drivers ↔ trailers ↔ documents for relationship queries"*  
  Add one demo query that uses it (e.g. "Which driver has the most maintenance incidents?")  
- **Option B — Cut:** Remove `graph/` from file tree in README if not implemented by demo time.  
  Do not leave unexplained modules in a hackathon repo.

---

## Gap 3 — Seed data volume too low for credibility
**Severity:** 🟠 High  
**Owner:** Charan (seed_data.py) + Yesh (synthetic_data_generator/)  

**Problem:**  
`seed_data.py` currently seeds 15+ documents. Statement 7 says an active fleet generates  
**50+ documents per week**. With only 15 documents, the hybrid query demo looks thin —  
especially queries like "How much did truck 84 spend on parts last month?" which need  
enough maintenance receipts to actually aggregate over.

**Fix:**  
- Target: **50–60 seeded documents** across at least 8 document types  
- Document types to cover: maintenance receipt, fuel record, title, registration,  
  tax form (IFTA), insurance certificate, inspection report, driver log  
- Spread across at least 10 trucks, 5 drivers, 4 trailers  
- At least 3 months of date coverage so time-range queries work

---

## Gap 4 — No hallucination prevention strategy documented or implemented
**Severity:** 🟠 High (statement explicitly calls this out)  
**Owner:** Teja (agents/, answer_generator.py)  

**Problem:**  
Statement 7 says *"accurately, grounded, no hallucinations"* — this is a judging criterion.  
The README shows source citations exist in the response schema, but never explains  
what happens when the system can't find an answer. Right now the LLM could fabricate  
an answer with no retrieved context and still return it confidently.

**Fix (implement in answer_generator.py):**  
```python
# If no sources retrieved above confidence threshold → return explicit fallback
if not sources or max(s["score"] for s in sources) < CONFIDENCE_THRESHOLD:
    return {
        "answer": "I couldn't find a document in the fleet records that answers this. "
                  "Try uploading the relevant document first.",
        "sources": [],
        "query_type": query_type
    }
```
- Set `CONFIDENCE_THRESHOLD = 0.65` as a starting point (tune during testing)  
- Add `CONFIDENCE_THRESHOLD` to `.env.example` and `config.py`  
- For SQL agent: if query returns 0 rows, return a natural language "no records found"  
  instead of letting the LLM guess  
- For hybrid: both legs must return results; if SQL returns 0 rows AND RAG score is low,  
  fall back cleanly

---

## Gap 5 — Synthetic documents are too clean (messiness not realistic)
**Severity:** 🟡 Medium (judges who read the statement will notice)  
**Owner:** Yesh (generate_documents.py) + Charan (ocr_processor.py)  

**Problem:**  
Statement 7 says *"the messiness should be realistic."* Current synthetic generator  
likely produces clean, well-structured PDFs. Real fleet documents are messy:  
handwritten maintenance receipts, faded fuel logs, scanned titles with OCR artifacts,  
inconsistent truck ID formats (Truck 84 vs TRK-084 vs truck84).

**Fix:**  
In `generate_documents.py`, add noise variants:  
- Inconsistent truck ID formats across documents (`Truck 84`, `TRK-084`, `Unit #84`)  
- At least 2 documents with intentional OCR-style typos (0 vs O, 1 vs I)  
- One multi-page PDF (maintenance history with 3–4 entries)  
- One document with a missing field (no date, or no driver name)  
- Mix of date formats: `06/15/2026`, `June 15 2026`, `2026-06-15`  

In `entity_linker.py`, normalize these variants before storing so all formats  
map to the same `truck_id` in the DB — this is actually a demo-worthy feature.

---

## Gap 6 — Profitability query requires cost aggregation across doc types (not wired yet)
**Severity:** 🟡 Medium  
**Owner:** Teja (sql_agent.py + hybrid_agent.py)  

**Problem:**  
Demo query: *"Which truck is most profitable this quarter?"*  
This requires joining: fuel records + maintenance receipts + (optionally) revenue data  
across multiple tables. The SQL schema needs to support this aggregation and  
`sql_agent.py` needs to generate the right multi-table query.

**Fix:**  
- Ensure `models.py` has a `costs` view or the SQL agent can join  
  `fuel_records`, `maintenance_records`, and `revenue_records` by `truck_id`  
- Add a "revenue" document type to synthetic data (load manifest or trip summary)  
- Test this specific query during integration — it's the most impressive demo moment  
  and also the most likely to break

---

## Summary checklist

| # | Gap | Severity | Owner | Status |
|---|-----|----------|-------|--------|
| 1 | Trailer entity missing | 🔴 Critical | Charan + Teja | ⬜ Open |
| 2 | Graph module undocumented | 🟠 High | Aryan + Teja | ⬜ Open |
| 3 | Seed data too low (15 → 50+) | 🟠 High | Charan + Yesh | ⬜ Open |
| 4 | No hallucination fallback | 🟠 High | Teja | ⬜ Open |
| 5 | Docs too clean / no messiness | 🟡 Medium | Yesh + Charan | ⬜ Open |
| 6 | Profitability query not wired | 🟡 Medium | Teja | ⬜ Open |

Update Status column to ✅ Done as each gap is closed.

---

*Raised by Teja — sync with team at next standup before build starts.*
