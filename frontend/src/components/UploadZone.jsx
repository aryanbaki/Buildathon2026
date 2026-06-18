import React, { useState, useRef } from "react";
import { uploadDocument } from "../services/api";

const ACCEPT = ".pdf,.jpg,.jpeg,.png,.docx,.txt,.csv";

export default function UploadZone({ trucks = [], onUploadComplete }) {
  const [dragging, setDragging] = useState(false);
  const [selectedTruck, setSelectedTruck] = useState("");
  const [uploads, setUploads] = useState([]);
  const inputRef = useRef(null);

  function handleDrop(e) {
    e.preventDefault();
    setDragging(false);
    processFiles(Array.from(e.dataTransfer.files));
  }

  function processFiles(files) {
    if (!selectedTruck) { alert("Select a truck first."); return; }
    files.forEach((file) => uploadFile(file));
  }

  async function uploadFile(file) {
    const id = crypto.randomUUID();
    setUploads((u) => [...u, { id, name: file.name, status: "uploading", progress: 0 }]);
    try {
      await uploadDocument(file, selectedTruck);
      setUploads((u) => u.map((x) => x.id === id ? { ...x, status: "done", progress: 100 } : x));
      onUploadComplete?.();
    } catch (e) {
      setUploads((u) => u.map((x) => x.id === id ? { ...x, status: "error", error: e.message } : x));
    }
  }

  const statusColor = { uploading: "#854F0B", done: "#0F6E56", error: "#A32D2D" };
  const statusLabel = { uploading: "Uploading…", done: "Ingested", error: "Failed" };

  return (
    <div>
      {/* Truck selector */}
      <div style={{ marginBottom: 12 }}>
        <label style={{ fontSize: 13, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>
          Link to truck
        </label>
        <select
          value={selectedTruck}
          onChange={(e) => setSelectedTruck(e.target.value)}
          style={{ width: "100%", fontSize: 14 }}
        >
          <option value="">Select truck…</option>
          {trucks.map((t) => (
            <option key={t.id} value={t.id}>
              Truck {t.unit_number} — {t.make} {t.model} {t.year}
            </option>
          ))}
        </select>
      </div>

      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        style={{
          border: `1.5px dashed ${dragging ? "#534AB7" : "var(--color-border-secondary, #ccc)"}`,
          borderRadius: 12,
          padding: "32px 24px",
          textAlign: "center",
          cursor: "pointer",
          background: dragging ? "#EEEDFE" : "var(--color-background-secondary)",
          transition: "all 0.15s",
        }}
      >
        <div style={{ fontSize: 28, marginBottom: 8 }}>📂</div>
        <div style={{ fontSize: 14, fontWeight: 500, color: "var(--color-text-primary)" }}>
          Drop documents here
        </div>
        <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginTop: 4 }}>
          PDF, JPG, PNG, DOCX, CSV — maintenance, fuel, registration, tax forms
        </div>
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPT}
          multiple
          style={{ display: "none" }}
          onChange={(e) => processFiles(Array.from(e.target.files))}
        />
      </div>

      {/* Upload list */}
      {uploads.length > 0 && (
        <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 6 }}>
          {uploads.map((u) => (
            <div key={u.id} style={{
              display: "flex", alignItems: "center", gap: 10,
              background: "var(--color-background-primary)",
              border: "0.5px solid var(--color-border-tertiary)",
              borderRadius: 8, padding: "8px 12px", fontSize: 13,
            }}>
              <span style={{ flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {u.name}
              </span>
              <span style={{
                fontSize: 11, fontWeight: 500,
                color: statusColor[u.status],
                background: u.status === "done" ? "#E1F5EE" : u.status === "error" ? "#FCEBEB" : "#FAEEDA",
                padding: "2px 8px", borderRadius: 20,
              }}>
                {statusLabel[u.status]}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
