"""Thin HTTP clients for the three live data sources the terminal uses:

- Finnhub: quotes, company profile/fundamentals, market news (needs FINNHUB_API_KEY)
- GoldAPI: gold/silver spot price (needs GOLDAPI_KEY)
- Yahoo Finance's public chart endpoint: historical daily closes, no key
  (same endpoint the `yfinance` library wraps; used only for the
  return/covariance calc, not quotes).

Every function returns raw provider JSON (already verified against the live
APIs) or raises httpx.HTTPError — callers decide how to handle a failed
symbol so one bad ticker doesn't take down a whole refresh.
"""

import httpx
from django.conf import settings

FINNHUB_BASE = "https://finnhub.io/api/v1"
GOLDAPI_BASE = "https://www.goldapi.io/api"
YAHOO_CHART_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"

_TIMEOUT = 10.0


def finnhub_quote(symbol: str) -> dict:
    resp = httpx.get(
        f"{FINNHUB_BASE}/quote",
        params={"symbol": symbol, "token": settings.FINNHUB_API_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def finnhub_profile(symbol: str) -> dict:
    resp = httpx.get(
        f"{FINNHUB_BASE}/stock/profile2",
        params={"symbol": symbol, "token": settings.FINNHUB_API_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def finnhub_metrics(symbol: str) -> dict:
    resp = httpx.get(
        f"{FINNHUB_BASE}/stock/metric",
        params={"symbol": symbol, "metric": "all", "token": settings.FINNHUB_API_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json().get("metric", {})


def finnhub_market_news() -> list[dict]:
    resp = httpx.get(
        f"{FINNHUB_BASE}/news",
        params={"category": "general", "token": settings.FINNHUB_API_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def goldapi_spot(metal: str) -> dict:
    """metal: 'XAU' (gold) or 'XAG' (silver)."""
    resp = httpx.get(
        f"{GOLDAPI_BASE}/{metal}/USD",
        headers={"x-access-token": settings.GOLDAPI_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def yahoo_daily_closes(symbol: str, range_: str = "6mo") -> dict:
    """Returns {"closes": [...], "volume": [...]} for the trailing `range_`."""
    resp = httpx.get(
        f"{YAHOO_CHART_BASE}/{symbol}",
        params={"range": range_, "interval": "1d"},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    result = resp.json()["chart"]["result"][0]
    quote = result["indicators"]["quote"][0]
    closes = [c for c in quote["close"] if c is not None]
    volumes = [v for v in quote["volume"] if v is not None]
    return {"closes": closes, "volume": volumes}
