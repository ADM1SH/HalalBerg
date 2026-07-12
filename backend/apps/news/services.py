import logging
import re
from datetime import datetime, timezone as dt_timezone

from django.core.cache import cache

from apps.market.providers import finnhub_market_news
from apps.market.symbols import SYMBOLS

from .models import NewsItem

logger = logging.getLogger(__name__)

NEWS_CACHE_KEY = "news_last_refreshed"
NEWS_STALE_SECONDS = 10 * 60
MAX_ITEMS = 40

# ponytail: lexicon-based heuristic, not an ML classifier — swap for a real
# sentiment model/LLM call if precision matters later.
POSITIVE_WORDS = {
    "beat", "beats", "surge", "surges", "soar", "soars", "rally", "rallies",
    "gain", "gains", "jump", "jumps", "record", "growth", "upgrade",
    "upgraded", "profit", "strong", "outperform", "rise", "rises", "boost",
    "boosts", "win", "wins", "positive", "higher", "advance", "advances",
    "beating", "expands", "expansion", "optimistic", "bullish",
}
NEGATIVE_WORDS = {
    "miss", "misses", "plunge", "plunges", "slump", "slumps", "fall",
    "falls", "drop", "drops", "decline", "declines", "cut", "cuts",
    "downgrade", "downgraded", "loss", "losses", "weak", "underperform",
    "lawsuit", "probe", "investigation", "recall", "layoffs", "negative",
    "lower", "warns", "warning", "scrutiny", "volatility", "bearish",
    "sues", "sued", "fraud", "crash", "crashes", "tumbles", "tumble",
}


def _classify_sentiment(text: str) -> str:
    words = set(text.lower().replace(",", " ").replace(".", " ").split())
    pos = len(words & POSITIVE_WORDS)
    neg = len(words & NEGATIVE_WORDS)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def _related_symbols(text: str) -> str:
    upper = text.upper()
    return ",".join(
        s for s in SYMBOLS if re.search(rf"\b{re.escape(s)}\b", upper)
    )


def refresh_news() -> None:
    try:
        articles = finnhub_market_news()
    except Exception:
        logger.exception("news refresh failed")
        return

    for article in articles[:MAX_ITEMS]:
        headline = article.get("headline") or ""
        summary = article.get("summary") or ""
        text = f"{headline} {summary}"
        published_at = datetime.fromtimestamp(
            article.get("datetime") or 0, tz=dt_timezone.utc
        )

        NewsItem.objects.update_or_create(
            external_id=article.get("id"),
            defaults={
                "headline": headline,
                "summary": summary,
                "source": article.get("source") or "",
                "url": article.get("url") or "",
                "published_at": published_at,
                "related_symbols": _related_symbols(text),
                "sentiment": _classify_sentiment(text),
            },
        )


def ensure_news_fresh() -> None:
    if cache.get(NEWS_CACHE_KEY) is None:
        refresh_news()
        cache.set(NEWS_CACHE_KEY, True, timeout=NEWS_STALE_SECONDS)
