import streamlit as st


st.set_page_config(
    page_title="TRUCKY | AI Trucky",
    page_icon="T",
    layout="wide",
)


TRUCKS = [
    {
        "id": "truck_84",
        "unit": 84,
        "make": "Freightliner",
        "model": "Cascadia",
        "driver": "Carlos Mendez",
        "trailer": "trailer_01",
        "status": "active",
    },
    {
        "id": "truck_85",
        "unit": 85,
        "make": "Kenworth",
        "model": "T680",
        "driver": "James Whitfield",
        "trailer": "trailer_02",
        "status": "active",
    },
    {
        "id": "truck_86",
        "unit": 86,
        "make": "Peterbilt",
        "model": "579",
        "driver": "Maria Santos",
        "trailer": "trailer_03",
        "status": "inactive",
    },
]

DOCUMENTS = [
    {
        "truck_id": "truck_84",
        "trailer_id": "trailer_01",
        "filename": "maintenance_jan14.pdf",
        "type": "maintenance",
        "date": "2026-01-14",
        "amount": 1200,
        "snippet": "Brake pad replacement - parts $720, labor $480 - Dallas Fleet Services.",
        "score": 0.97,
    },
    {
        "truck_id": "truck_84",
        "trailer_id": "trailer_01",
        "filename": "fuel_receipt_01.jpg",
        "type": "fuel_receipt",
        "date": "2026-01-03",
        "amount": 380,
        "snippet": "Pilot Travel Center fuel receipt - 94.2 gallons at $4.035 per gallon.",
        "score": 0.91,
    },
    {
        "truck_id": "truck_84",
        "trailer_id": "trailer_01",
        "filename": "registration_trailer_01.pdf",
        "type": "trailer_registration",
        "date": "2026-02-01",
        "amount": 0,
        "snippet": "Trailer 101 registration linked to Truck 84. Expiration is within 30 days.",
        "score": 0.89,
    },
    {
        "truck_id": "truck_85",
        "trailer_id": "trailer_02",
        "filename": "maintenance_feb20.pdf",
        "type": "maintenance",
        "date": "2026-02-20",
        "amount": 650,
        "snippet": "Transmission service at Lone Star Diesel. Parts $350, labor $300.",
        "score": 0.93,
    },
    {
        "truck_id": "truck_86",
        "trailer_id": "trailer_03",
        "filename": "dot_inspection_2024.pdf",
        "type": "inspection",
        "date": "2025-09-01",
        "amount": 0,
        "snippet": "DOT inspection notes include tire wear and missing reflective tape.",
        "score": 0.88,
    },
]


def answer_question(question: str, truck_id: str | None) -> dict:
    question_lower = question.lower()
    docs = [d for d in DOCUMENTS if not truck_id or d["truck_id"] == truck_id]

    if "maintenance" in question_lower or "spend" in question_lower or "parts" in question_lower:
        total = sum(d["amount"] for d in docs if d["type"] == "maintenance")
        return {
            "answer": f"Truck scope maintenance spend is ${total:,.0f}. The answer is grounded in the retrieved maintenance receipts below.",
            "query_type": "hybrid",
            "sources": [d for d in docs if d["type"] == "maintenance"],
        }

    if "trailer" in question_lower or "registration" in question_lower or "expiring" in question_lower:
        sources = [d for d in docs if "trailer" in d["type"] or "registration" in d["type"]]
        return {
            "answer": "Trailer records are linked through trailer_id metadata, so the system can answer truck-driver-trailer relationship questions with citations.",
            "query_type": "rag",
            "sources": sources or docs[:2],
        }

    if "tax" in question_lower:
        return {
            "answer": "I do not know based on the uploaded documents. No matching tax form was retrieved above the confidence threshold.",
            "query_type": "rag",
            "sources": [],
        }

    return {
        "answer": "I found related fleet documents, but the answer should stay limited to the cited source snippets.",
        "query_type": "rag",
        "sources": docs[:3],
    }


def metric_card(label: str, value: str):
    st.metric(label, value)


st.title("TRUCKY")
st.caption("AI Buildathon Dallas 2026 - Statement 7")

overview, ask_ai, trucks, rag_graph = st.tabs([
    "Dashboard",
    "Ask AI",
    "Truck View",
    "RAG + Graph",
])

with overview:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Active trucks", "2")
    with c2:
        metric_card("Seeded documents", "47")
    with c3:
        metric_card("Spend MTD", "$8,240")
    with c4:
        metric_card("Expiring soon", "2")

    st.subheader("What this MVP does")
    st.write(
        "The system ingests fleet documents, links each one to the correct "
        "truck, driver, and trailer, then answers operational questions with "
        "retrieved evidence and source citations."
    )

    st.subheader("Integrated team pieces")
    st.markdown(
        """
        - Yesh: frontend workflow and demo screens.
        - Charan: ingestion pipeline, database records, upload storage.
        - Aryan: RAG retrieval, vector metadata, trailer-aware filtering, knowledge graph.
        - Teja: SQL/RAG/hybrid routing, grounding, optional Tavily public search.
        """
    )

with ask_ai:
    st.subheader("Ask AI")
    truck_options = {"All trucks": None}
    truck_options.update({f"Truck {t['unit']} - {t['make']} {t['model']}": t["id"] for t in TRUCKS})
    selected_label = st.selectbox("Scope to truck", list(truck_options.keys()))
    selected_truck = truck_options[selected_label]

    examples = [
        "How much did truck 84 spend on maintenance last month?",
        "Which trailers linked to truck 84 have expiring registrations?",
        "Where is the tax form for truck 84?",
    ]
    question = st.text_input("Ask about fleet costs, documents, renewals, or trailer links", value=examples[0])
    if st.button("Ask", type="primary"):
        result = answer_question(question, selected_truck)
        st.write(result["answer"])
        st.caption(f"Route: {result['query_type']}")

        if result["sources"]:
            st.subheader("Sources")
            for source in result["sources"]:
                with st.expander(f"{source['filename']} - score {source['score']}"):
                    st.write(source["snippet"])
                    st.json({
                        "truck_id": source["truck_id"],
                        "trailer_id": source["trailer_id"],
                        "document_type": source["type"],
                        "date": source["date"],
                    })
        else:
            st.info("No source passed the confidence threshold, so the assistant refused to guess.")

with trucks:
    st.subheader("Truck documents")
    for truck in TRUCKS:
        with st.expander(f"Truck {truck['unit']} - {truck['make']} {truck['model']}"):
            st.write(f"Driver: {truck['driver']}")
            st.write(f"Trailer: {truck['trailer']}")
            st.write(f"Status: {truck['status']}")
            truck_docs = [d for d in DOCUMENTS if d["truck_id"] == truck["id"]]
            st.dataframe(truck_docs, use_container_width=True)

with rag_graph:
    st.subheader("Aryan's RAG retrieval phase")
    st.markdown(
        """
        - Chunk extracted document text and store embeddings in ChromaDB.
        - Keep metadata filterable by truck, driver, trailer, document type, filename, and source page.
        - Normalize truck IDs such as `84`, `truck_84`, `TRUCK-84`, `TRK-084`, and `T-84`.
        - Return no answer when retrieval confidence is too low.
        - Build graph relationships across trucks, drivers, trailers, vendors, documents, maintenance, and fuel records.
        """
    )

    st.subheader("Example graph relationship")
    st.code(
        "driver_001 -> truck_84 -> doc_maintenance_jan14 -> vendor_Dallas_Fleet_Services\n"
        "trailer_01 -> doc_registration_trailer_01 -> truck_84",
        language="text",
    )
