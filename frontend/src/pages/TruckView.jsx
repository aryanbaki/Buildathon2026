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
    <div className="page-wrap">
      <header className="page-hero">
        <div>
          <span className="eyebrow">Truck command view</span>
          <h1>Truck view</h1>
          <p>Review truck metadata, linked documents, and truck-scoped AI answers.</p>
        </div>
      </header>

      {/* Truck selector row */}
      <div className="truck-selector">
        {trucks.map((t) => (
          <button
            key={t.id}
            onClick={() => setSelectedId(t.id)}
            className={selectedId === t.id ? "active" : ""}
          >
            Truck {t.unit_number}
            <span>{t.make}</span>
          </button>
        ))}
      </div>

      {selected && (
        <div className="truck-view-grid">
          {/* Left: truck info + docs */}
          <div>
            {/* Truck card */}
            <div className="surface-panel truck-info-card">
              <h2>Truck {selected.unit_number}</h2>
              <div className="info-grid">
                {[
                  ["Make", selected.make],
                  ["Model", selected.model],
                  ["Year", selected.year],
                  ["Status", selected.status],
                ].map(([k, v]) => (
                  <div key={k}>
                    <span>{k}</span>
                    <strong>{v}</strong>
                  </div>
                ))}
              </div>
            </div>

            {/* Documents */}
            <div className="section-label">
              {docs.length} documents
            </div>
            {loading ? (
              <div className="empty-state">Loading documents...</div>
            ) : (
              <div className="document-list">
                {docs.map((d) => <DocumentCard key={d.id} doc={d} colors={DOC_TYPE_COLORS} />)}
              </div>
            )}
          </div>

          {/* Right: AI chat scoped to this truck */}
          <div className="surface-panel chat-surface">
            <div className="section-label">
              Ask about truck {selected.unit_number}
            </div>
            <ChatPanel selectedTruckId={selectedId} />
          </div>
        </div>
      )}
    </div>
  );
}
