"""Curated watchlist the terminal tracks. Free-tier data providers can't
screen the whole market on demand, so this is a fixed universe rather than
a live search — add tickers here to track more.

# ponytail: capped at 25 symbols, not "all stocks" — a quotes refresh makes
# 2 Finnhub calls/symbol (quote + profile), and the free Finnhub tier caps
# out at 60 calls/minute. 25 symbols = 50 calls, safely under that ceiling
# with room for the shariah/news calls that can land in the same window.
# Raise this only alongside a paid tier or a rate limiter in providers.py.
"""

SYMBOLS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "TSLA",
    "PG",
    "JNJ",
    "JPM",
    "BAC",
    "XOM",
    "KO",
    "DIS",
    "PFE",
    "V",
    "META",
    "NFLX",
    "INTC",
    "WMT",
    "HD",
    "NKE",
    "CAT",
    "MS",
    "T",
    "CMCSA",
]
