"""
Gold app — stores live spot gold and silver prices from GoldAPI.io.
Used for:
  1. Zakat Nisab calculation (85g gold threshold)
  2. Ticker tape display (GC=F equivalent)
  3. MYR Nisab = gold_price_per_gram_usd × usd_myr_rate × 85
"""

from django.db import models


class GoldPrice(models.Model):
    """
    Live gold and silver spot prices fetched from GoldAPI.io.
    Stored every 5 minutes by APScheduler background task.
    """
    # Timestamp of the fetch
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    # Gold prices
    gold_price_usd_troy = models.DecimalField(
        max_digits=14, decimal_places=4,
        help_text="Gold spot price per troy oz (31.1035g) in USD."
    )
    gold_price_usd_gram = models.DecimalField(
        max_digits=14, decimal_places=4,
        help_text="Gold spot price per gram in USD."
    )
    gold_prev_close_usd = models.DecimalField(
        max_digits=14, decimal_places=4,
        null=True, blank=True,
        help_text="Gold previous close price in USD."
    )
    gold_change_usd = models.DecimalField(
        max_digits=12, decimal_places=4,
        null=True, blank=True,
        help_text="Gold price change from previous close (USD)."
    )
    gold_change_pct = models.DecimalField(
        max_digits=8, decimal_places=4,
        null=True, blank=True,
        help_text="Gold price percentage change from previous close."
    )

    # Silver prices (for reference / Zakat alternative)
    silver_price_usd_troy = models.DecimalField(
        max_digits=14, decimal_places=4,
        null=True, blank=True,
        help_text="Silver spot price per troy oz in USD."
    )
    silver_price_usd_gram = models.DecimalField(
        max_digits=14, decimal_places=4,
        null=True, blank=True,
        help_text="Silver spot price per gram in USD."
    )

    # USD/MYR exchange rate at time of fetch (sourced from yfinance USDMYR=X)
    usd_myr_rate = models.DecimalField(
        max_digits=10, decimal_places=4,
        null=True, blank=True,
        help_text="USD to MYR exchange rate at fetch time."
    )

    # Derived Nisab values (computed and stored for fast access)
    nisab_usd = models.DecimalField(
        max_digits=14, decimal_places=4,
        null=True, blank=True,
        help_text="Nisab in USD = gold_price_per_gram_usd × 85g."
    )
    nisab_myr = models.DecimalField(
        max_digits=14, decimal_places=4,
        null=True, blank=True,
        help_text="Nisab in MYR = nisab_usd × usd_myr_rate."
    )

    class Meta:
        ordering = ["-timestamp"]
        get_latest_by = "timestamp"
        verbose_name = "Gold Price"
        verbose_name_plural = "Gold Prices"

    def __str__(self):
        return (
            f"Gold ${float(self.gold_price_usd_troy):,.2f}/oz "
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')} UTC]"
        )

    @property
    def gold_price_myr_gram(self):
        """Returns gold price per gram in MYR (if exchange rate available)."""
        if not self.usd_myr_rate:
            return None
        return float(self.gold_price_usd_gram) * float(self.usd_myr_rate)
