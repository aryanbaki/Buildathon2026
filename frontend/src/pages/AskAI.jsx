import { useState } from "react";
import { getTrucks } from "../services/api";
import { useEffect } from "react";
import ChatPanel from "../components/ChatPanel";

export default function AskAI() {
  const [trucks, setTrucks] = useState([]);
  const [selectedTruckId, setSelectedTruckId] = useState(null);

  useEffect(() => { getTrucks().then(setTrucks); }, []);

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: "24px 20px" }}>
      <h1 style={{ fontSize: 22, fontWeight: 500, margin: "0 0 4px" }}>Ask AI</h1>
      <p style={{ fontSize: 14, color: "var(--color-text-secondary)", margin: "0 0 20px" }}>
        Every answer is grounded in a real document or database row — no hallucinations.
      </p>

      {/* Optional truck filter */}
      <div style={{ marginBottom: 16, display: "flex", alignItems: "center", gap: 10 }}>
        <span style={{ fontSize: 13, color: "var(--color-text-secondary)" }}>Scope to truck</span>
        <select
          value={selectedTruckId || ""}
          onChange={(e) => setSelectedTruckId(e.target.value || null)}
          style={{ fontSize: 13 }}
        >
          <option value="">All trucks</option>
          {trucks.map((t) => (
            <option key={t.id} value={t.id}>Truck {t.unit_number} — {t.make} {t.model}</option>
          ))}
        </select>
      </div>

      <div style={{
        background: "var(--color-background-primary,#fff)",
        border: "0.5px solid var(--color-border-tertiary,#e0dfd8)",
        borderRadius: 12, padding: 20,
      }}>
        <ChatPanel selectedTruckId={selectedTruckId} />
      </div>
    </div>
  );
}
