import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

const NAV_TOP = [
  { to: "/dashboard", label: "Dashboard", icon: "⬡" },
  { to: "/ask",       label: "Ask AI",    icon: "◎" },
  { to: "/trucks",    label: "Trucks",    icon: "▣" },
];

const NAV_BOTTOM = [
  { to: "/about",    label: "About",    icon: "◈" },
  { to: "/contact",  label: "Contact",  icon: "✉" },
  { to: "/settings", label: "Settings", icon: "⚙" },
];

const linkStyle = (isActive) => ({
  display: "flex", alignItems: "center", gap: 10,
  padding: "9px 12px", borderRadius: 10, marginBottom: 2,
  fontSize: 13, fontWeight: isActive ? 600 : 400,
  textDecoration: "none",
  color: isActive ? "#fff" : "#9898B0",
  background: isActive ? "rgba(244,166,34,.15)" : "transparent",
  borderLeft: isActive ? "2px solid #F4A622" : "2px solid transparent",
  transition: "all .15s",
});

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside style={{
      width: 215, minHeight: "100vh", background: "#1A1A2E",
      display: "flex", flexDirection: "column", flexShrink: 0,
      borderRight: "1px solid rgba(255,255,255,.06)",
    }}>
      {/* Logo */}
      <div style={{ padding: "22px 18px 18px", borderBottom: "1px solid rgba(255,255,255,.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 30, height: 30, background: "#F4A622", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15 }}>🚛</div>
          <div>
            <div style={{ color: "#E8E8F0", fontSize: 13, fontWeight: 600 }}>Fleet AI</div>
            <div style={{ color: "#9898B0", fontSize: 11 }}>Document Intelligence</div>
          </div>
        </div>
      </div>

      {/* Main nav */}
      <nav style={{ padding: "10px 8px" }}>
        {NAV_TOP.map(({ to, label, icon }) => (
          <NavLink key={to} to={to} style={({ isActive }) => linkStyle(isActive)}>
            <span style={{ fontSize: 15 }}>{icon}</span>{label}
          </NavLink>
        ))}
      </nav>

      <div style={{ flex: 1 }} />

      {/* Bottom nav */}
      <nav style={{ padding: "0 8px 8px", borderTop: "1px solid rgba(255,255,255,.06)", paddingTop: 8 }}>
        {NAV_BOTTOM.map(({ to, label, icon }) => (
          <NavLink key={to} to={to} style={({ isActive }) => linkStyle(isActive)}>
            <span style={{ fontSize: 15 }}>{icon}</span>{label}
          </NavLink>
        ))}
      </nav>

      {/* User */}
      {user && (
        <div style={{ padding: "14px 16px", borderTop: "1px solid rgba(255,255,255,.06)", display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 30, height: 30, borderRadius: "50%", background: "#F4A622",
            color: "#fff", display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 12, fontWeight: 700, flexShrink: 0,
          }}>{user.avatar || user.name?.[0]}</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ color: "#E8E8F0", fontSize: 12, fontWeight: 500, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{user.name}</div>
            <div style={{ color: "#9898B0", fontSize: 10 }}>{user.role?.replace("_"," ")}</div>
          </div>
          <button onClick={logout} title="Sign out" style={{ background: "none", border: "none", color: "#9898B0", cursor: "pointer", fontSize: 14, flexShrink: 0 }}>⏻</button>
        </div>
      )}
    </aside>
  );
}
