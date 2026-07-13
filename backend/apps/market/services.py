"""Keeps Quote rows fresh from Finnhub/Yahoo. No scheduler/Celery — each
view calls ensure_quotes_fresh() before reading, so the first request after
the TTL expires pays one refresh and everything else is a fast DB read.
"""

import logging
from concurrent.futures import ThreadPoolExecutor

from django.utils import timezone

from .models import Quote
from .providers import PROFILE_CACHE_SECONDS, finnhub_profile, finnhub_quote, yahoo_daily_closes
from .symbols import SYMBOLS

logger = logging.getLogger(__name__)

QUOTE_STALE_SECONDS = PROFILE_CACHE_SECONDS


def quotes_are_stale() -> bool:
    latest = Quote.objects.order_by("-updated_at").values_list(
        "updated_at", flat=True
    ).first()
    if latest is None:
        return True
    return (timezone.now() - latest).total_seconds() > QUOTE_STALE_SECONDS


def _fetch_quote(symbol: str) -> tuple[str, dict] | None:
    try:
        quote_data = finnhub_quote(symbol)
        profile_data = finnhub_profile(symbol)
        volumes = yahoo_daily_closes(symbol, range_="5d")["volume"]
    except Exception:
        logger.exception("market refresh failed for %s", symbol)
        return None

    return symbol, {
        "name": profile_data.get("name") or symbol,
        "sector": profile_data.get("finnhubIndustry") or "Unknown",
        "price": quote_data.get("c") or 0,
        "change": quote_data.get("d") or 0,
        "change_percent": quote_data.get("dp") or 0,
        "volume": volumes[-1] if volumes else 0,
        "market_cap": int(
            (profile_data.get("marketCapitalization") or 0) * 1_000_000
        ),
    }


def refresh_quotes() -> None:
    # I/O-bound (waiting on Finnhub/Yahoo), so a thread pool works despite
    # the GIL — cuts a 15-symbol refresh from ~30s sequential to a few
    # seconds. SQLite writes happen back on the main thread.
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = pool.map(_fetch_quote, SYMBOLS)

    for result in results:
        if result is None:
            continue
        symbol, defaults = result
        Quote.objects.update_or_create(symbol=symbol, defaults=defaults)


def ensure_quotes_fresh() -> None:
    if quotes_are_stale():
        refresh_quotes()
