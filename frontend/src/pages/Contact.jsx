import React, { useState } from "react";

export default function Contact() {
  const [form, setForm]       = useState({ name: "", email: "", subject: "", message: "" });
  const [status, setStatus]   = useState("");
  const [loading, setLoading] = useState(false);

  function update(k, v) { setForm(f => ({ ...f, [k]: v })); }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.name || !form.email || !form.message) { setStatus("error"); return; }
    setLoading(true);
    await new Promise(r => setTimeout(r, 1200));
    setLoading(false);
    setStatus("sent");
    setForm({ name: "", email: "", subject: "", message: "" });
  }

  const inputStyle = {
    width: "100%", padding: "10px 14px", fontSize: 14,
    border: "1px solid #E4E2D9", borderRadius: 8,
    outline: "none", background: "#FAFAFA",
  };
  const labelStyle = { display: "block", fontSize: 12, fontWeight: 600, color: "#6B6965", marginBottom: 6, textTransform: "uppercase", letterSpacing: ".05em" };

  return (
    <div style={{ padding: "32px 40px", maxWidth: 900 }}>
      <div style={{ marginBottom: 28 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: "#F4A622", letterSpacing: ".12em", textTransform: "uppercase", marginBottom: 6 }}>Get in touch</div>
        <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8 }}>Contact us</h1>
        <p style={{ fontSize: 14, color: "#6B6965" }}>Have a question about Fleet AI? Reach out and we'll get back to you.</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        {/* Form */}
        <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, padding: "24px 28px" }}>
          {status === "sent" ? (
            <div style={{ textAlign: "center", padding: "32px 0" }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>✅</div>
              <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 8 }}>Message sent!</div>
              <div style={{ fontSize: 13, color: "#6B6965" }}>We'll get back to you within 24 hours.</div>
              <button onClick={() => setStatus("")} style={{ marginTop: 20, padding: "9px 20px", background: "#F4A622", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
                Send another
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
                <div>
                  <label style={labelStyle}>Name</label>
                  <input value={form.name} onChange={e => update("name", e.target.value)} placeholder="Your name" style={inputStyle} />
                </div>
                <div>
                  <label style={labelStyle}>Email</label>
                  <input type="email" value={form.email} onChange={e => update("email", e.target.value)} placeholder="you@company.com" style={inputStyle} />
                </div>
              </div>
              <div style={{ marginBottom: 14 }}>
                <label style={labelStyle}>Subject</label>
                <select value={form.subject} onChange={e => update("subject", e.target.value)} style={inputStyle}>
                  <option value="">Select a topic…</option>
                  <option>General inquiry</option>
                  <option>Bug report</option>
                  <option>Feature request</option>
                  <option>Demo request</option>
                  <option>Partnership</option>
                </select>
              </div>
              <div style={{ marginBottom: 16 }}>
                <label style={labelStyle}>Message</label>
                <textarea
                  value={form.message} onChange={e => update("message", e.target.value)}
                  placeholder="Tell us what's on your mind…" rows={5}
                  style={{ ...inputStyle, resize: "vertical", lineHeight: 1.6 }}
                />
              </div>
              {status === "error" && (
                <div style={{ fontSize: 12, color: "#DC2626", background: "#FEE2E2", border: "1px solid #FECACA", borderRadius: 8, padding: "8px 12px", marginBottom: 12 }}>
                  Please fill in all required fields.
                </div>
              )}
              <button type="submit" disabled={loading} style={{ width: "100%", padding: "11px", background: "#1A1A2E", color: "#fff", border: "none", borderRadius: 8, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
                {loading ? "Sending…" : "Send message"}
              </button>
            </form>
          )}
        </div>

        {/* Info cards */}
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          {[
            { icon: "✉️", label: "Email", value: "yeshsalapu2@gmail.com", sub: "Response within 24 hours" },
            { icon: "💼", label: "LinkedIn", value: "linkedin.com/in/yeshsalapu", sub: "Connect with the team" },
            { icon: "💻", label: "GitHub", value: "github.com/aryanbaki/Buildathon2026", sub: "View the source code" },
            { icon: "📍", label: "Location", value: "Irving, TX", sub: "AI Buildathon Dallas 2026" },
          ].map(({ icon, label, value, sub }) => (
            <div key={label} style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 12, padding: "16px 20px", display: "flex", gap: 14, alignItems: "flex-start" }}>
              <span style={{ fontSize: 22, flexShrink: 0 }}>{icon}</span>
              <div>
                <div style={{ fontSize: 12, fontWeight: 600, color: "#9C9890", textTransform: "uppercase", letterSpacing: ".05em", marginBottom: 3 }}>{label}</div>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{value}</div>
                <div style={{ fontSize: 12, color: "#9C9890" }}>{sub}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
