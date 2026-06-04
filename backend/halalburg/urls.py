"""
HalalBurg Terminal — Root URL Configuration
All API routes are prefixed with /api/
"""

from django.urls import path, include

urlpatterns = [
    # Market data: quotes, OHLCV history, ticker search, index tape
    path("api/market/", include("apps.market.urls")),

    # Fundamentals: income statements, balance sheets, cash flows (FMP)
    path("api/fundamentals/", include("apps.fundamentals.urls")),

    # Shariah: audit engine and screener
    path("api/shariah/", include("apps.shariah.urls")),

    # Portfolio: holdings CRUD and Zakat calculation
    path("api/portfolio/", include("apps.portfolio.urls")),

    # News: NewsAPI cached headlines
    path("api/news/", include("apps.news.urls")),

    # Gold: GoldAPI spot prices for Nisab calculation
    path("api/gold/", include("apps.gold.urls")),

    # AI: LM Studio summarisation pipe
    path("api/ai/", include("apps.ai_summary.urls")),
]
