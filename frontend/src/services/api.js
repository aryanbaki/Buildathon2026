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

const MOCK_TRUCKS = [
  { id: "truck_84", unit_number: 84, make: "Freightliner", model: "Cascadia", year: 2019, status: "active" },
  { id: "truck_85", unit_number: 85, make: "Kenworth", model: "T680", year: 2020, status: "active" },
  { id: "truck_86", unit_number: 86, make: "Peterbilt", model: "579", year: 2018, status: "inactive" },
  { id: "truck_87", unit_number: 87, make: "Freightliner", model: "Columbia", year: 2017, status: "active" },
  { id: "truck_88", unit_number: 88, make: "Kenworth", model: "W900", year: 2021, status: "active" },
  { id: "truck_89", unit_number: 89, make: "Peterbilt", model: "389", year: 2022, status: "active" },
  { id: "truck_90", unit_number: 90, make: "Freightliner", model: "M2", year: 2016, status: "active" },
  { id: "truck_91", unit_number: 91, make: "Kenworth", model: "T880", year: 2019, status: "active" },
  { id: "truck_92", unit_number: 92, make: "Peterbilt", model: "567", year: 2018, status: "inactive" },
  { id: "truck_93", unit_number: 93, make: "Freightliner", model: "Cascadia", year: 2023, status: "active" },
];

const MOCK_DOCUMENTS = [
  { id: "doc_001", filename: "maintenance_history_multipage.txt", doc_type: "maintenance", doc_date: "2026-05-12", amount: 1325.72, vendor: "Dallas Fleet Services" },
  { id: "doc_002", filename: "fuel_missing_date.txt", doc_type: "fuel_receipt", doc_date: null, amount: 429.85, vendor: "Pilot Travel Center" },
  { id: "doc_003", filename: "form_2290_2025.txt", doc_type: "tax_form", doc_date: "2025-08-31", amount: 550, vendor: "IRS" },
  { id: "doc_004", filename: "registration.txt", doc_type: "registration", doc_date: "2025-08-22", expiry_date: "2026-08-22", amount: 847 },
  { id: "doc_005", filename: "inspection_2026.txt", doc_type: "inspection", doc_date: "2026-03-04", vendor: "TX DOT Inspector" },
];

async function fetchJson(path, fallback) {
  if (MOCK_MODE) return fallback;

  try {
    const res = await fetch(`${BASE_URL}${path}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  } catch (error) {
    console.warn(`Using demo fallback for ${path}:`, error.message);
    return fallback;
  }
}

export async function askQuestion(question, truckId = null) {
  if (MOCK_MODE) {
    await new Promise((r) => setTimeout(r, 900));
    return MOCK_ANSWER;
  }
  try {
    const res = await fetch(`${BASE_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, truck_id: truckId }),
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  } catch (error) {
    console.warn("Using demo fallback for /ask:", error.message);
    return MOCK_ANSWER;
  }
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
  return fetchJson("/trucks", MOCK_TRUCKS);
}

export async function getTruckDocuments(truckId) {
  return fetchJson(`/trucks/${truckId}/documents`, MOCK_DOCUMENTS);
}

export async function getFleetStats() {
  return fetchJson("/stats", { total_trucks: 10, total_documents: 141, total_spend_mtd: 8240, expiring_soon: 2 });
}
