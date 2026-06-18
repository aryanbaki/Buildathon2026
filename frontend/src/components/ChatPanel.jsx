import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../services/api";

function SourceCard({ source }) {
  return (
    <div style={{
      background: "var(--color-background-secondary, #f5f5f3)",
      border: "0.5px solid var(--color-border-tertiary, #e0dfd8)",
      borderRadius: 8,
      padding: "8px 12px",
      fontSize: 12,
      marginTop: 6,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 2 }}>
        <span style={{ fontWeight: 500 }}>{source.filename}</span>
        <span style={{ color: "#888", fontSize: 11 }}>
          {Math.round(source.score * 100)}% match
        </span>
      </div>
      <div style={{ color: "#666", lineHeight: 1.5 }}>{source.snippet}</div>
      <div style={{ marginTop: 4, fontSize: 11, color: "#999" }}>
        Truck {source.truck_id?.replace("truck_", "")}
      </div>
    </div>
  );
}

function QueryTypeBadge({ type }) {
  const colors = {
    sql: { bg: "#E1F5EE", color: "#0F6E56" },
    rag: { bg: "#EEEDFE", color: "#534AB7" },
    hybrid: { bg: "#FAEEDA", color: "#854F0B" },
  };
  const c = colors[type] || colors.hybrid;
  return (
    <span style={{
      background: c.bg, color: c.color,
      fontSize: 10, fontWeight: 500,
      padding: "2px 8px", borderRadius: 20,
      marginLeft: 8, verticalAlign: "middle",
    }}>
      {type}
    </span>
  );
}

export default function ChatPanel({ selectedTruckId }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Ask me anything about your fleet — costs, documents, maintenance history, renewals.",
      sources: [],
      query_type: null,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const q = input.trim();
    if (!q || loading) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", text: q }]);
    setLoading(true);
    try {
      const data = await askQuestion(q, selectedTruckId);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          text: data.answer,
          sources: data.sources || [],
          query_type: data.query_type,
          sql_query: data.sql_query,
        },
      ]);
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: "assistant", text: `Error: ${e.message}`, sources: [], query_type: null },
      ]);
    } finally {
      setLoading(false);
    }
  }

  const SUGGESTIONS = [
    "How much did truck 84 spend on maintenance last month?",
    "Which trucks have registrations expiring soon?",
    "Where's the tax form for truck 84?",
    "Which truck is most profitable?",
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", minHeight: 500 }}>
      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px 0", display: "flex", flexDirection: "column", gap: 12 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
            <div style={{ maxWidth: "80%" }}>
              <div style={{
                background: m.role === "user" ? "#534AB7" : "var(--color-background-primary, #fff)",
                color: m.role === "user" ? "#fff" : "inherit",
                border: m.role === "user" ? "none" : "0.5px solid var(--color-border-tertiary, #e0dfd8)",
                borderRadius: m.role === "user" ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
                padding: "10px 14px",
                fontSize: 14,
                lineHeight: 1.6,
              }}>
                {m.text}
                {m.query_type && <QueryTypeBadge type={m.query_type} />}
              </div>
              {m.sql_query && (
                <div style={{
                  marginTop: 6, fontSize: 11,
                  background: "#1e1e2e", color: "#a6e3a1",
                  borderRadius: 6, padding: "6px 10px",
                  fontFamily: "monospace",
                }}>
                  {m.sql_query}
                </div>
              )}
              {m.sources?.length > 0 && (
                <div style={{ marginTop: 4 }}>
                  <div style={{ fontSize: 11, color: "#999", marginBottom: 2 }}>Sources</div>
                  {m.sources.map((s, j) => <SourceCard key={j} source={s} />)}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: "flex", gap: 4, padding: "10px 14px" }}>
            {[0, 1, 2].map((i) => (
              <div key={i} style={{
                width: 7, height: 7, borderRadius: "50%",
                background: "#534AB7", opacity: 0.6,
                animation: `bounce 1s ease-in-out ${i * 0.15}s infinite`,
              }} />
            ))}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Suggestions */}
      {messages.length === 1 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, padding: "8px 0" }}>
          {SUGGESTIONS.map((s, i) => (
            <button key={i} onClick={() => setInput(s)} style={{
              fontSize: 12, padding: "4px 10px",
              border: "0.5px solid var(--color-border-secondary, #ccc)",
              borderRadius: 20, background: "transparent",
              cursor: "pointer", color: "var(--color-text-secondary)",
            }}>
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div style={{ display: "flex", gap: 8, paddingTop: 12, borderTop: "0.5px solid var(--color-border-tertiary, #e0dfd8)" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder={selectedTruckId ? `Ask about ${selectedTruckId}…` : "Ask about your fleet…"}
          style={{ flex: 1, fontSize: 14, padding: "8px 12px", borderRadius: 8 }}
        />
        <button onClick={handleSend} disabled={loading || !input.trim()} style={{
          padding: "8px 16px", borderRadius: 8, background: "#534AB7",
          color: "#fff", border: "none", cursor: "pointer", fontSize: 14,
          opacity: loading || !input.trim() ? 0.5 : 1,
        }}>
          Ask
        </button>
      </div>

      <style>{`@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }`}</style>
    </div>
  );
}
