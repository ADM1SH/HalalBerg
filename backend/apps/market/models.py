"""
Market app — stores live quotes and OHLCV price history.
Data source: yfinance (no API key required).
"""

from django.db import models


class Ticker(models.Model):
    """
    Master ticker registry. Every other model FK's back to this.
    The `symbol` field stores the yfinance-format symbol
    (e.g., AAPL, ASML, 1818.KL for Bursa Malaysia).
    """
    symbol = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200, blank=True)
    exchange = models.CharField(max_length=50, blank=True)   # NASDAQ, KLSE, NYSE, etc.
    sector = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    currency = models.CharField(max_length=10, blank=True)   # USD, MYR, EUR, etc.
    market_cap = models.BigIntegerField(null=True, blank=True)
    is_etf = models.BooleanField(default=False)
    is_bursa = models.BooleanField(default=False)   # True for .KL tickers

    # Live quote fields (refreshed by APScheduler background task)
    last_price = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    price_change = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    pct_change = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    day_high = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    day_low = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    week_52_high = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    week_52_low = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    eps = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    beta = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["symbol"]
        verbose_name = "Ticker"
        verbose_name_plural = "Tickers"

    def __str__(self):
        return f"{self.symbol} ({self.name})"

    @property
    def display_symbol(self):
        """Returns clean display symbol (strips .KL suffix for display)."""
        if self.is_bursa and self.symbol.endswith(".KL"):
            return self.symbol[:-3]
        return self.symbol


class PriceHistory(models.Model):
    """
    OHLCV daily price history for chart rendering.
    Cached locally to minimise yfinance API calls.
    """
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name="prices")
    date = models.DateField(db_index=True)
    open = models.DecimalField(max_digits=18, decimal_places=4)
    high = models.DecimalField(max_digits=18, decimal_places=4)
    low = models.DecimalField(max_digits=18, decimal_places=4)
    close = models.DecimalField(max_digits=18, decimal_places=4)
    volume = models.BigIntegerField()
    adj_close = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)

    class Meta:
        unique_together = ("ticker", "date")
        ordering = ["-date"]
        verbose_name = "Price History"

    def __str__(self):
        return f"{self.ticker.symbol} {self.date} close={self.close}"


class WatchlistItem(models.Model):
    """
    User watchlist entries. Single-user app so no user FK needed.
    Multiple named watchlists supported via `list_name`.
    """
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name="watchlist_items")
    list_name = models.CharField(max_length=100, default="Default")
    added_at = models.DateTimeField(auto_now_add=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        unique_together = ("ticker", "list_name")
        ordering = ["list_name", "sort_order", "ticker__symbol"]

    def __str__(self):
        return f"[{self.list_name}] {self.ticker.symbol}"
