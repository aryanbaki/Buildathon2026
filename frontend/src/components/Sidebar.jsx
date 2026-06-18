import { NavLink } from "react-router-dom";

const NAV = [
  { to: "/dashboard", label: "Dashboard", icon: "⬡" },
  { to: "/ask",       label: "Ask AI",    icon: "◎" },
  { to: "/trucks",    label: "Trucks",    icon: "▣" },
];

export default function Sidebar() {
  return (
    <aside style={{
      width: 210, minHeight: "100vh", background: "#1A1A2E",
      display: "flex", flexDirection: "column", flexShrink: 0,
      borderRight: "1px solid rgba(255,255,255,.06)",
    }}>
      <div style={{ padding: "22px 18px 18px", borderBottom: "1px solid rgba(255,255,255,.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 30, height: 30, background: "#F4A622", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15 }}>🚛</div>
          <div>
            <div style={{ color: "#E8E8F0", fontSize: 13, fontWeight: 600 }}>Fleet AI</div>
            <div style={{ color: "#9898B0", fontSize: 11 }}>Document Intelligence</div>
          </div>
        </div>
      </div>
      <nav style={{ padding: "10px 8px", flex: 1 }}>
        {NAV.map(({ to, label, icon }) => (
          <NavLink key={to} to={to} style={({ isActive }) => ({
            display: "flex", alignItems: "center", gap: 10,
            padding: "9px 12px", borderRadius: 10, marginBottom: 2,
            fontSize: 13, fontWeight: 500, textDecoration: "none",
            color: isActive ? "#fff" : "#9898B0",
            background: isActive ? "rgba(244,166,34,.15)" : "transparent",
            borderLeft: isActive ? "2px solid #F4A622" : "2px solid transparent",
          })}>
            <span style={{ fontSize: 15 }}>{icon}</span>{label}
          </NavLink>
        ))}
      </nav>
      <div style={{ padding: "14px 18px", borderTop: "1px solid rgba(255,255,255,.06)" }}>
        <div style={{ fontSize: 11, color: "#9898B0" }}>Yesh · Charan · Aryan · Teja</div>
        <div style={{ fontSize: 11, color: "#9898B0", marginTop: 2 }}>Buildathon Dallas 2026</div>
      </div>
    </aside>
  );
}
