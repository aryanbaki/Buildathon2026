import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext.jsx";
import Sidebar from "./components/Sidebar.jsx";
import Landing from "./pages/Landing.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AskAI from "./pages/AskAI.jsx";
import TruckView from "./pages/TruckView.jsx";
import About from "./pages/About.jsx";
import Contact from "./pages/Contact.jsx";
import Settings from "./pages/Settings.jsx";

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function ProtectedShell({ children }) {
  return (
    <ProtectedRoute>
      <div className="app-shell">
        <Sidebar />
        <main className="app-main">{children}</main>
      </div>
    </ProtectedRoute>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/about" element={<About isPublic />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<ProtectedShell><Dashboard /></ProtectedShell>} />
          <Route path="/ask" element={<ProtectedShell><AskAI /></ProtectedShell>} />
          <Route path="/trucks" element={<ProtectedShell><TruckView /></ProtectedShell>} />
          <Route path="/trucks/:truckId" element={<ProtectedShell><TruckView /></ProtectedShell>} />
          <Route path="/contact" element={<ProtectedShell><Contact /></ProtectedShell>} />
          <Route path="/settings" element={<ProtectedShell><Settings /></ProtectedShell>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
