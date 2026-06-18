import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext.jsx";
import LoginModal from "./components/LoginModal.jsx";
import Sidebar from "./components/Sidebar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AskAI from "./pages/AskAI.jsx";
import TruckView from "./pages/TruckView.jsx";
import About from "./pages/About.jsx";
import Contact from "./pages/Contact.jsx";
import Settings from "./pages/Settings.jsx";

function AppShell() {
  const { user, showLogin } = useAuth();
  return (
    <>
      {showLogin && <LoginModal />}
      <div style={{ display: "flex", minHeight: "100vh", filter: showLogin ? "blur(3px)" : "none", transition: "filter .2s" }}>
        <Sidebar />
        <main style={{ flex: 1, overflowY: "auto", minHeight: "100vh" }}>
          <Routes>
            <Route path="/"              element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard"     element={<Dashboard />} />
            <Route path="/ask"           element={<AskAI />} />
            <Route path="/trucks"        element={<TruckView />} />
            <Route path="/trucks/:truckId" element={<TruckView />} />
            <Route path="/about"         element={<About />} />
            <Route path="/contact"       element={<Contact />} />
            <Route path="/settings"      element={<Settings />} />
          </Routes>
        </main>
      </div>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppShell />
      </BrowserRouter>
    </AuthProvider>
  );
}
