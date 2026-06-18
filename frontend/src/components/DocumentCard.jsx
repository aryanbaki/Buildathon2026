// DocumentCard.jsx
import React from "react";

export default function DocumentCard({ doc, colors = {} }) {
  const c = colors[doc.doc_type] || { bg: "#F1EFE8", color: "#5F5E5A" };
  const isExpiringSoon = doc.expiry_date && (
    (new Date(doc.expiry_date) - new Date()) / (1000 * 60 * 60 * 24) < 30
  );

  return (
    <div style={{
      background: "var(--color-background-primary,#fff)",
      border: `0.5px solid ${isExpiringSoon ? "#F09595" : "var(--color-border-tertiary,#e0dfd8)"}`,
      borderRadius: 8, padding: "10px 14px",
      display: "flex", alignItems: "center", gap: 10,
    }}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 13, fontWeight: 500, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {doc.filename}
        </div>
        <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginTop: 2 }}>
          {doc.doc_date}
          {doc.amount && ` · $${doc.amount.toLocaleString()}`}
          {doc.expiry_date && ` · expires ${doc.expiry_date}`}
        </div>
      </div>
      <span style={{
        fontSize: 10, fontWeight: 500, padding: "2px 8px", borderRadius: 20,
        background: c.bg, color: c.color, whiteSpace: "nowrap",
      }}>
        {doc.doc_type.replace("_", " ")}
      </span>
      {isExpiringSoon && (
        <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 20, background: "#FCEBEB", color: "#A32D2D", fontWeight: 500 }}>
          expiring
        </span>
      )}
    </div>
  );
}
