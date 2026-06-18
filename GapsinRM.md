# TRUCKY - Known Gaps and Fix Tracker

## Summary checklist

| # | Gap | Severity | Owner | Status |
|---|-----|----------|-------|--------|
| 1 | Trailer entity missing | Critical | Charan + Teja + Aryan | Partial (Teja routing + Aryan retrieval done) |
| 2 | Graph module undocumented | High | Aryan + Teja | Done in `README.md` |
| 3 | Seed data too low | High | Charan + Yesh | Open |
| 4 | No hallucination fallback | High | Teja | Done |
| 5 | Docs too clean | Medium | Yesh + Charan | Open |
| 6 | Profitability query not wired | Medium | Teja | Done |

Teja branch closes gaps 4 and 6, partial gap 1, and merges Aryan RAG retrieval. Aryan branch documents the graph module, adds trailer-aware RAG metadata, and keeps the graph scope tied to truck/driver/trailer/document relationships.
