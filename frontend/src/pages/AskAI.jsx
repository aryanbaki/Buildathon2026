import { useState } from "react";
import { getTrucks } from "../services/api";
import { useEffect } from "react";
import ChatPanel from "../components/ChatPanel";

export default function AskAI() {
  const [trucks, setTrucks] = useState([]);
  const [selectedTruckId, setSelectedTruckId] = useState(null);

  useEffect(() => { getTrucks().then(setTrucks); }, []);

  return (
    <div className="page-wrap narrow-page">
      <header className="page-hero">
        <div>
          <span className="eyebrow">Grounded fleet assistant</span>
          <h1>Ask AI</h1>
          <p>Every answer is grounded in a real document or database row.</p>
        </div>
      </header>

      {/* Optional truck filter */}
      <div className="filter-row">
        <span>Scope to truck</span>
        <select
          value={selectedTruckId || ""}
          onChange={(e) => setSelectedTruckId(e.target.value || null)}
        >
          <option value="">All trucks</option>
          {trucks.map((t) => (
            <option key={t.id} value={t.id}>Truck {t.unit_number} — {t.make} {t.model}</option>
          ))}
        </select>
      </div>

      <div className="surface-panel chat-surface">
        <ChatPanel selectedTruckId={selectedTruckId} />
      </div>
    </div>
  );
}
