import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AskAI from "./pages/AskAI.jsx";
import TruckView from "./pages/TruckView.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: "flex", minHeight: "100vh" }}>
        <Sidebar />
        <main style={{ flex: 1, overflowY: "auto" }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/ask" element={<AskAI />} />
            <Route path="/trucks" element={<TruckView />} />
            <Route path="/trucks/:truckId" element={<TruckView />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
