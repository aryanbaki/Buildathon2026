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
  padding: "10px 12px", borderRadius: 8, marginBottom: 4,
  fontSize: 13, fontWeight: isActive ? 600 : 400,
  textDecoration: "none",
  color: isActive ? "#ecfdf5" : "#93a39a",
  background: isActive ? "linear-gradient(135deg, rgba(21,128,61,.25), rgba(245,158,11,.08))" : "transparent",
  border: isActive ? "1px solid rgba(52,211,153,.24)" : "1px solid transparent",
  boxShadow: isActive ? "0 10px 26px rgba(0,0,0,.24)" : "none",
  transition: "all .18s ease",
});

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside style={{
      width: 236, minHeight: "100vh", background: "linear-gradient(180deg, #04120d 0%, #071812 48%, #030806 100%)",
      display: "flex", flexDirection: "column", flexShrink: 0,
      borderRight: "1px solid rgba(52,211,153,.12)",
    }}>
      {/* Logo */}
      <div style={{ padding: "22px 18px 18px", borderBottom: "1px solid rgba(52,211,153,.10)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 34, height: 34, background: "linear-gradient(135deg, #22c55e, #f59e0b)", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 800, color: "#03130c" }}>FM</div>
          <div>
            <div style={{ color: "#ecfdf5", fontSize: 14, fontWeight: 700 }}>FleetMind AI</div>
            <div style={{ color: "#93a39a", fontSize: 11 }}>Document intelligence</div>
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
      <nav style={{ padding: "0 8px 8px", borderTop: "1px solid rgba(52,211,153,.10)", paddingTop: 8 }}>
        {NAV_BOTTOM.map(({ to, label, icon }) => (
          <NavLink key={to} to={to} style={({ isActive }) => linkStyle(isActive)}>
            <span style={{ fontSize: 15 }}>{icon}</span>{label}
          </NavLink>
        ))}
      </nav>

      {/* User */}
      {user && (
        <div style={{ padding: "14px 16px", borderTop: "1px solid rgba(52,211,153,.10)", display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 30, height: 30, borderRadius: "50%", background: "#22c55e",
            color: "#03130c", display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 12, fontWeight: 700, flexShrink: 0,
          }}>{user.avatar || user.name?.[0]}</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ color: "#ecfdf5", fontSize: 12, fontWeight: 600, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{user.name}</div>
            <div style={{ color: "#93a39a", fontSize: 10 }}>{user.role?.replace("_"," ")}</div>
          </div>
          <button onClick={logout} title="Sign out" style={{ background: "none", border: "none", color: "#93a39a", cursor: "pointer", fontSize: 14, flexShrink: 0 }}>⏻</button>
        </div>
      )}
    </aside>
  );
}
