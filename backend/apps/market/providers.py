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

import threading
import time

import httpx
from django.conf import settings
from django.core.cache import cache

FINNHUB_BASE = "https://finnhub.io/api/v1"
GOLDAPI_BASE = "https://www.goldapi.io/api"
YAHOO_CHART_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"

_TIMEOUT = 10.0
# Also used by apps.market.services.QUOTE_STALE_SECONDS — quotes and shariah
# refreshes both call finnhub_profile per symbol, and on a cold cache they
# can land in the same request.
PROFILE_CACHE_SECONDS = 60

# Free-tier Finnhub caps out at 60 calls/minute. Threaded refreshes across a
# growing symbol universe can burst past that (confirmed: 429s on a 25-symbol
# cold start), so every Finnhub call is throttled through one shared gate
# instead of relying on the symbol count staying under some hand-picked
# threshold — this stays correct as SYMBOLS grows.
# ponytail: fixed-interval gate, not a sliding-window limiter — good enough
# for one process; swap for a token bucket if calls ever come from multiple
# workers.
_FINNHUB_MIN_INTERVAL = 60.0 / 55  # ~1.09s/call, a small buffer under 60/min
_finnhub_lock = threading.Lock()
_last_finnhub_call = 0.0


def _throttle_finnhub() -> None:
    global _last_finnhub_call
    with _finnhub_lock:
        wait = _last_finnhub_call + _FINNHUB_MIN_INTERVAL - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last_finnhub_call = time.monotonic()


def finnhub_quote(symbol: str) -> dict:
    _throttle_finnhub()
    resp = httpx.get(
        f"{FINNHUB_BASE}/quote",
        params={"symbol": symbol, "token": settings.FINNHUB_API_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def finnhub_profile(symbol: str) -> dict:
    cache_key = f"finnhub_profile:{symbol}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    _throttle_finnhub()
    resp = httpx.get(
        f"{FINNHUB_BASE}/stock/profile2",
        params={"symbol": symbol, "token": settings.FINNHUB_API_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    cache.set(cache_key, data, timeout=PROFILE_CACHE_SECONDS)
    return data


def finnhub_metrics(symbol: str) -> dict:
    _throttle_finnhub()
    resp = httpx.get(
        f"{FINNHUB_BASE}/stock/metric",
        params={"symbol": symbol, "metric": "all", "token": settings.FINNHUB_API_KEY},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json().get("metric", {})


def finnhub_market_news() -> list[dict]:
    _throttle_finnhub()
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
