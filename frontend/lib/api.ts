const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

async function get<T>(path: string, signal?: AbortSignal): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, { signal });
  if (!res.ok) {
    throw new Error(`GET ${path} failed with ${res.status}`);
  }
  return res.json() as Promise<T>;
}

async function post<TBody, TResponse>(
  path: string,
  body: TBody,
  signal?: AbortSignal
): Promise<TResponse> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
  if (!res.ok) {
    throw new Error(`POST ${path} failed with ${res.status}`);
  }
  return res.json() as Promise<TResponse>;
}

export const api = {
  quotes: (signal?: AbortSignal) => get("/market/quotes/", signal),
  quote: (symbol: string, signal?: AbortSignal) =>
    get(`/market/quotes/${symbol}/`, signal),
  shariahAssessments: (signal?: AbortSignal) =>
    get("/shariah/assessments/", signal),
  shariahAssessment: (symbol: string, signal?: AbortSignal) =>
    get(`/shariah/assessments/${symbol}/`, signal),
  goldSilverSpot: (signal?: AbortSignal) => get("/gold/spot/", signal),
  nisab: (signal?: AbortSignal) => get("/gold/nisab/", signal),
  news: (signal?: AbortSignal) => get("/news/feed/", signal),
  risk: (signal?: AbortSignal) => get("/news/risk/", signal),
  portfolio: (signal?: AbortSignal) => get("/portfolio/summary/", signal),
  screener: (params: string, signal?: AbortSignal) =>
    get(`/shariah/screener/?${params}`, signal),
  efficientFrontier: <TBody, TResponse>(body: TBody, signal?: AbortSignal) =>
    post<TBody, TResponse>("/quant/efficient-frontier/", body, signal),
  blackScholes: <TBody, TResponse>(body: TBody, signal?: AbortSignal) =>
    post<TBody, TResponse>("/quant/black-scholes/", body, signal),
};

export { API_BASE_URL };
