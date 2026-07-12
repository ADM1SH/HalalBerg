"""Approximate AAOIFI-style Shariah screen computed from live Finnhub
fundamentals. Not a certified Shariah ruling — a free-tier data source
doesn't expose a clean "interest income" line item, so interest_income_ratio
and non_compliant_income_ratio are left at 0 (unavailable at this tier) and
the business-activity sector screen is the primary gate for financial-sector
exclusion, backed by the two ratios that ARE derivable: debt/market-cap and
liquid-assets/market-cap.
"""

import logging
from concurrent.futures import ThreadPoolExecutor

from django.utils import timezone

from apps.market.models import Quote
from apps.market.providers import finnhub_metrics, finnhub_profile
from apps.market.services import ensure_quotes_fresh
from apps.market.symbols import SYMBOLS

from .models import ShariahAssessment

logger = logging.getLogger(__name__)

ASSESSMENT_STALE_SECONDS = 6 * 60 * 60

EXCLUDED_INDUSTRIES = {
    "Banking",
    "Insurance",
    "Diversified Financial Services",
    "Consumer Finance",
    "Investment Banking/Brokerage",
    "Asset Management",
    "Beverages - Alcoholic",
    "Casinos/Gaming",
}

RATIO_LIMIT = 0.33
QUESTIONABLE_BAND = 0.03


def assessments_are_stale() -> bool:
    latest = ShariahAssessment.objects.order_by("-updated_at").values_list(
        "updated_at", flat=True
    ).first()
    if latest is None:
        return True
    return (timezone.now() - latest).total_seconds() > ASSESSMENT_STALE_SECONDS


def _compute_ratios(symbol: str, market_cap: float) -> tuple[float, float]:
    metrics = finnhub_metrics(symbol)
    profile = finnhub_profile(symbol)

    shares_outstanding = (profile.get("shareOutstanding") or 0) * 1_000_000
    book_value_per_share = metrics.get("bookValuePerShareQuarterly") or 0
    debt_to_equity = metrics.get("totalDebt/totalEquityQuarterly") or 0
    cash_per_share = metrics.get("cashPerSharePerShareQuarterly") or 0

    total_equity = book_value_per_share * shares_outstanding
    total_debt = debt_to_equity * total_equity
    total_cash = cash_per_share * shares_outstanding

    debt_ratio = total_debt / market_cap if market_cap else 0.0
    liquid_ratio = total_cash / market_cap if market_cap else 0.0
    return debt_ratio, liquid_ratio


def _fetch_ratios(symbol: str, market_cap: float) -> tuple[str, float, float] | None:
    try:
        debt_ratio, liquid_ratio = _compute_ratios(symbol, market_cap)
    except Exception:
        logger.exception("shariah refresh failed for %s", symbol)
        return None
    return symbol, debt_ratio, liquid_ratio


def refresh_assessments() -> None:
    ensure_quotes_fresh()

    quotes_by_symbol = {q.symbol: q for q in Quote.objects.filter(symbol__in=SYMBOLS)}

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = pool.map(
            lambda symbol: _fetch_ratios(
                symbol, quotes_by_symbol[symbol].market_cap
            ),
            quotes_by_symbol.keys(),
        )

    for result in results:
        if result is None:
            continue
        symbol, debt_ratio, liquid_ratio = result
        quote = quotes_by_symbol[symbol]

        sector_excluded = quote.sector in EXCLUDED_INDUSTRIES
        worst_ratio = max(debt_ratio, liquid_ratio)

        if sector_excluded:
            status = "non_compliant"
            reason = (
                f"Business-activity screen: {quote.sector} is a core "
                "interest-based/excluded sector under AAOIFI guidelines."
            )
        elif worst_ratio > RATIO_LIMIT + QUESTIONABLE_BAND:
            status = "non_compliant"
            reason = "Exceeds the 33% AAOIFI debt/liquid-assets ratio ceiling."
        elif worst_ratio > RATIO_LIMIT - QUESTIONABLE_BAND:
            status = "questionable"
            reason = "Near the 33% AAOIFI debt/liquid-assets ratio ceiling."
        else:
            status = "compliant"
            reason = "Within AAOIFI debt/liquid-assets ratio limits."

        notes = (
            f"{reason} Debt/market-cap {debt_ratio:.1%}, "
            f"liquid-assets/market-cap {liquid_ratio:.1%}. Approximate "
            "screen from reported financials, not a certified Shariah "
            "ruling — non-core income isn't exposed at this data tier, so "
            "the business-activity screen is the primary gate for "
            "financial-sector exclusion."
        )

        ShariahAssessment.objects.update_or_create(
            quote=quote,
            defaults={
                "status": status,
                "debt_to_market_cap": round(debt_ratio, 4),
                "liquid_assets_ratio": round(liquid_ratio, 4),
                "interest_income_ratio": 0.0,
                "non_compliant_income_ratio": 0.0,
                "notes": notes,
            },
        )
        Quote.objects.filter(symbol=symbol).update(
            is_shariah_compliant=(status == "compliant")
        )


def ensure_assessments_fresh() -> None:
    if assessments_are_stale():
        refresh_assessments()
