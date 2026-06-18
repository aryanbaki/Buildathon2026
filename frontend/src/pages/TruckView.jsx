import { useState, useEffect } from "react";
import { getTrucks, getTruckDocuments } from "../services/api";
import ChatPanel from "../components/ChatPanel";
import DocumentCard from "../components/DocumentCard";

const DOC_TYPE_COLORS = {
  maintenance:   { bg: "#FAEEDA", color: "#854F0B" },
  fuel_receipt:  { bg: "#E1F5EE", color: "#0F6E56" },
  registration:  { bg: "#EEEDFE", color: "#534AB7" },
  insurance:     { bg: "#E6F1FB", color: "#185FA5" },
  tax_form:      { bg: "#FAECE7", color: "#993C1D" },
  inspection:    { bg: "#EAF3DE", color: "#3B6D11" },
  other:         { bg: "#F1EFE8", color: "#5F5E5A" },
};

export default function TruckView() {
  const [trucks, setTrucks] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getTrucks().then((t) => { setTrucks(t); if (t.length) setSelectedId(t[0].id); });
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    setLoading(true);
    getTruckDocuments(selectedId).then((d) => { setDocs(d); setLoading(false); });
  }, [selectedId]);

  const selected = trucks.find((t) => t.id === selectedId);

  return (
    <div style={{ maxWidth: 960, margin: "0 auto", padding: "24px 20px" }}>
      <h1 style={{ fontSize: 22, fontWeight: 500, margin: "0 0 16px" }}>Truck view</h1>

      {/* Truck selector row */}
      <div style={{ display: "flex", gap: 10, marginBottom: 20, flexWrap: "wrap" }}>
        {trucks.map((t) => (
          <button
            key={t.id}
            onClick={() => setSelectedId(t.id)}
            style={{
              padding: "8px 16px", borderRadius: 8, fontSize: 14, cursor: "pointer",
              border: selectedId === t.id ? "1.5px solid #534AB7" : "0.5px solid var(--color-border-tertiary,#e0dfd8)",
              background: selectedId === t.id ? "#EEEDFE" : "var(--color-background-primary,#fff)",
              color: selectedId === t.id ? "#534AB7" : "var(--color-text-primary)",
              fontWeight: selectedId === t.id ? 500 : 400,
            }}
          >
            Truck {t.unit_number}
            <span style={{ fontSize: 11, marginLeft: 6, color: "var(--color-text-secondary)" }}>
              {t.make}
            </span>
          </button>
        ))}
      </div>

      {selected && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {/* Left: truck info + docs */}
          <div>
            {/* Truck card */}
            <div style={{
              background: "var(--color-background-primary,#fff)",
              border: "0.5px solid var(--color-border-tertiary,#e0dfd8)",
              borderRadius: 12, padding: "16px 20px", marginBottom: 16,
            }}>
              <div style={{ fontSize: 18, fontWeight: 500, marginBottom: 8 }}>
                Truck {selected.unit_number}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px 16px", fontSize: 13 }}>
                {[
                  ["Make", selected.make],
                  ["Model", selected.model],
                  ["Year", selected.year],
                  ["Status", selected.status],
                ].map(([k, v]) => (
                  <div key={k}>
                    <span style={{ color: "var(--color-text-secondary)" }}>{k} </span>
                    <span style={{ fontWeight: 500 }}>{v}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Documents */}
            <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 8, color: "var(--color-text-secondary)" }}>
              {docs.length} documents
            </div>
            {loading ? (
              <div style={{ fontSize: 13, color: "var(--color-text-secondary)" }}>Loading…</div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {docs.map((d) => <DocumentCard key={d.id} doc={d} colors={DOC_TYPE_COLORS} />)}
              </div>
            )}
          </div>

          {/* Right: AI chat scoped to this truck */}
          <div style={{
            background: "var(--color-background-primary,#fff)",
            border: "0.5px solid var(--color-border-tertiary,#e0dfd8)",
            borderRadius: 12, padding: 16,
          }}>
            <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 12, color: "var(--color-text-secondary)" }}>
              Ask about truck {selected.unit_number}
            </div>
            <ChatPanel selectedTruckId={selectedId} />
          </div>
        </div>
      )}
    </div>
  );
}
