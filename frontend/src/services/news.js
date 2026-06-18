const TAVILY_KEY = import.meta.env.VITE_TAVILY_API_KEY;

const FALLBACK_NEWS = [
  { title: "Trucking freight rates stabilize amid strong Q2 demand", source: "FreightWaves", date: "Jun 18, 2026", tag: "Market", url: "https://freightwaves.com" },
  { title: "FMCSA proposes updated hours-of-service rule changes", source: "TruckingInfo", date: "Jun 18, 2026", tag: "Regulation", url: "https://truckinginfo.com" },
  { title: "Diesel prices dip below $3.80 in Texas and Southeast", source: "EIA", date: "Jun 18, 2026", tag: "Fuel", url: "https://eia.gov" },
  { title: "AI-powered fleet management adoption surges in 2026", source: "FleetOwner", date: "Jun 18, 2026", tag: "Tech", url: "https://fleetowner.com" },
  { title: "NHTSA issues recall notice for Freightliner brake systems", source: "NHTSA", date: "Jun 17, 2026", tag: "Safety", url: "https://nhtsa.gov" },
];

const TAG_MAP = (title) => {
  const t = title.toLowerCase();
  if (t.includes("fuel") || t.includes("diesel") || t.includes("price")) return "Fuel";
  if (t.includes("fmcsa") || t.includes("dot") || t.includes("rule") || t.includes("regulation")) return "Regulation";
  if (t.includes("recall") || t.includes("safety") || t.includes("nhtsa")) return "Safety";
  if (t.includes("ai") || t.includes("tech") || t.includes("electric") || t.includes("ev")) return "Tech";
  if (t.includes("rate") || t.includes("freight") || t.includes("market") || t.includes("demand")) return "Market";
  return "Industry";
};

export async function fetchTruckingNews() {
  if (!TAVILY_KEY) return FALLBACK_NEWS;

  try {
    const res = await fetch("https://api.tavily.com/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        api_key: TAVILY_KEY,
        query: "trucking industry news freight rates regulations 2026",
        search_depth: "basic",
        max_results: 6,
        include_domains: [
          "freightwaves.com", "truckinginfo.com", "fleetowner.com",
          "overdriveonline.com", "trucknews.com", "eia.gov",
          "fmcsa.dot.gov", "nhtsa.gov", "ttnews.com"
        ],
      }),
    });

    const data = await res.json();
    if (!data.results?.length) return FALLBACK_NEWS;

    return data.results.map((r) => ({
      title:   r.title,
      source:  new URL(r.url).hostname.replace("www.", ""),
      date:    new Date(r.published_date || Date.now()).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }),
      tag:     TAG_MAP(r.title),
      url:     r.url,
      snippet: r.content?.slice(0, 120) + "…",
    }));
  } catch (e) {
    return FALLBACK_NEWS;
  }
}
