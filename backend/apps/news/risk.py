"""Geopolitical risk signal computed from the live news feed already
flowing through this app (apps.news.services).

Conceptually inspired by World Monitor (https://github.com/koala73/worldmonitor
by Elie Habib, AGPL-3.0) — specifically its cross-stream signal correlation
and Country Instability Index ideas. This is an independent, much simpler
reimplementation: a keyword + sentiment weighted score over real Finnhub
headlines already stored in NewsItem. No World Monitor code, data, or
algorithm details were copied — see their repo for the real thing.
"""

from django.utils import timezone

from .models import NewsItem
from .services import ensure_news_fresh

CATEGORY_KEYWORDS = {
    "military": {
        "war", "strike", "strikes", "missile", "troops", "invasion",
        "airstrike", "offensive", "ceasefire", "conflict", "military",
        "navy", "combat", "attack",
    },
    "economic": {
        "sanctions", "embargo", "tariff", "oil", "opec", "inflation",
        "recession", "default", "currency", "supply", "shortage",
    },
    "disaster": {
        "earthquake", "flood", "wildfire", "hurricane", "explosion",
        "disaster", "evacuate", "evacuation", "tsunami",
    },
    "escalation": {
        "nuclear", "threat", "threatens", "warns", "warning",
        "retaliation", "mobilize", "blockade", "closed",
    },
}

# ponytail: negative headlines count double toward the score, positive
# count half — a coarse proxy for severity, not a calibrated risk model.
SENTIMENT_WEIGHT = {"negative": 2, "neutral": 1, "positive": 0.5}

LEVEL_THRESHOLDS = [(25, "low"), (50, "elevated"), (75, "high"), (101, "critical")]

# Saturating scale: this many weighted keyword hits across the sampled
# window maxes the score out at 100.
SATURATION_POINT = 40


def _score_article(headline: str, summary: str) -> tuple[int, set[str]]:
    words = set(f"{headline} {summary}".lower().replace(",", " ").replace(".", " ").split())
    hit_categories = {
        category for category, keywords in CATEGORY_KEYWORDS.items() if words & keywords
    }
    hits = sum(len(words & keywords) for keywords in CATEGORY_KEYWORDS.values())
    return hits, hit_categories


def compute_risk_signal(limit: int = 30) -> dict:
    ensure_news_fresh()
    articles = NewsItem.objects.all()[:limit]

    category_counts = {c: 0 for c in CATEGORY_KEYWORDS}
    scored = []
    raw_total = 0.0

    for article in articles:
        hits, categories = _score_article(article.headline, article.summary)
        if hits == 0:
            continue
        weighted = hits * SENTIMENT_WEIGHT.get(article.sentiment, 1)
        raw_total += weighted
        for category in categories:
            category_counts[category] += 1
        scored.append((weighted, article, sorted(categories)))

    escalation_score = min(100, round(raw_total / SATURATION_POINT * 100))
    level = next(name for threshold, name in LEVEL_THRESHOLDS if escalation_score < threshold)

    scored.sort(key=lambda item: item[0], reverse=True)
    top_signals = [
        {
            "headline": article.headline,
            "source": article.source,
            "url": article.url,
            "published_at": article.published_at,
            "categories": categories,
        }
        for _, article, categories in scored[:5]
    ]

    return {
        "escalation_score": escalation_score,
        "level": level,
        "categories": category_counts,
        "top_signals": top_signals,
        "as_of": timezone.now(),
    }
