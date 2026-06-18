const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const MOCK_MODE = import.meta.env.VITE_MOCK_API === "true";

const MOCK_ANSWER = {
  answer:
    "Truck 84 spent $3,420 on maintenance in January. The highest cost was a brake pad replacement ($1,200) at Dallas Fleet Services on Jan 14.",
  query_type: "hybrid",
  sql_query:
    "SELECT SUM(total_cost) FROM maintenance_records WHERE truck_id='truck_84' AND EXTRACT(MONTH FROM service_date)=1",
  sources: [
    {
      doc_id: "doc_001",
      filename: "maintenance_jan.pdf",
      truck_id: "truck_84",
      snippet: "Brake pad replacement — $1,200 — Dallas Fleet Services — Jan 14 2026",
      score: 0.97,
    },
    {
      doc_id: "doc_002",
      filename: "fuel_receipt_01.jpg",
      truck_id: "truck_84",
      snippet: "Oil change and filter — $380 — Quick Lube Irving — Jan 3 2026",
      score: 0.91,
    },
  ],
};

export async function askQuestion(question, truckId = null) {
  if (MOCK_MODE) {
    await new Promise((r) => setTimeout(r, 900));
    return MOCK_ANSWER;
  }
  const res = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, truck_id: truckId }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function uploadDocument(file, truckId) {
  const form = new FormData();
  form.append("file", file);
  form.append("truck_id", truckId);
  const res = await fetch(`${BASE_URL}/upload`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json();
}

export async function getTrucks() {
  if (MOCK_MODE) {
    return [
      { id: "truck_84", unit_number: 84, make: "Freightliner", model: "Cascadia", year: 2019, status: "active" },
      { id: "truck_85", unit_number: 85, make: "Kenworth", model: "T680", year: 2020, status: "active" },
      { id: "truck_86", unit_number: 86, make: "Peterbilt", model: "579", year: 2018, status: "inactive" },
    ];
  }
  const res = await fetch(`${BASE_URL}/trucks`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getTruckDocuments(truckId) {
  if (MOCK_MODE) {
    return [
      { id: "doc_001", filename: "maintenance_jan.pdf", doc_type: "maintenance", doc_date: "2026-01-14", amount: 1200 },
      { id: "doc_002", filename: "fuel_receipt_01.jpg", doc_type: "fuel_receipt", doc_date: "2026-01-03", amount: 380 },
      { id: "doc_003", filename: "registration.pdf", doc_type: "registration", doc_date: "2026-01-01", expiry_date: "2027-01-01" },
    ];
  }
  const res = await fetch(`${BASE_URL}/trucks/${truckId}/documents`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getFleetStats() {
  if (MOCK_MODE) {
    return { total_trucks: 3, total_documents: 47, total_spend_mtd: 8240, expiring_soon: 2 };
  }
  const res = await fetch(`${BASE_URL}/stats`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
