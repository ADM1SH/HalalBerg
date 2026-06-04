"""
Portfolio app — user holdings and Zakat calculation.
Single-user local app: no User FK needed.

Zakat formula:
  nisab_threshold = 85g × gold_price_per_gram (in MYR or USD)
  If portfolio_value >= nisab_threshold:
      zakat_due = portfolio_value × 0.025 (2.5%)
"""

from django.db import models
from apps.market.models import Ticker


class Holding(models.Model):
    """
    A single stock holding in the user's portfolio.
    Multiple entries for the same ticker are allowed (dollar-cost averaging).
    """
    ticker = models.ForeignKey(
        Ticker,
        on_delete=models.CASCADE,
        related_name="holdings",
    )
    quantity = models.DecimalField(
        max_digits=18, decimal_places=6,
        help_text="Number of shares/units held."
    )
    avg_cost = models.DecimalField(
        max_digits=18, decimal_places=4,
        help_text="Average cost per share in the ticker's native currency."
    )
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ticker__symbol", "purchase_date"]
        verbose_name = "Holding"
        verbose_name_plural = "Holdings"

    def __str__(self):
        return f"{float(self.quantity):.2f} × {self.ticker.symbol} @ {self.avg_cost}"

    @property
    def cost_basis(self):
        """Total cost basis = quantity × avg_cost."""
        return float(self.quantity) * float(self.avg_cost)

    @property
    def current_value(self):
        """Current market value = quantity × last_price (if available)."""
        if self.ticker.last_price is None:
            return None
        return float(self.quantity) * float(self.ticker.last_price)

    @property
    def unrealised_pnl(self):
        """Unrealised profit/loss in native currency."""
        cv = self.current_value
        if cv is None:
            return None
        return cv - self.cost_basis

    @property
    def unrealised_pnl_pct(self):
        """Unrealised P&L as a percentage."""
        pnl = self.unrealised_pnl
        if pnl is None or self.cost_basis == 0:
            return None
        return (pnl / self.cost_basis) * 100


class ZakatRecord(models.Model):
    """
    Saved Zakat calculation snapshot.
    Records the gold price, Nisab threshold, portfolio value, and Zakat due
    at the time of calculation.
    Supports both MYR and USD.
    """
    CURRENCY_MYR = "MYR"
    CURRENCY_USD = "USD"
    CURRENCY_CHOICES = [
        (CURRENCY_MYR, "Malaysian Ringgit (MYR)"),
        (CURRENCY_USD, "US Dollar (USD)"),
    ]

    calculated_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=CURRENCY_MYR)

    # Gold price used for Nisab calculation
    gold_price_per_gram = models.DecimalField(
        max_digits=14, decimal_places=4,
        help_text="Live gold price per gram in the selected currency."
    )
    gold_price_per_troy_oz = models.DecimalField(
        max_digits=14, decimal_places=4,
        help_text="Live gold price per troy oz (31.1035g) in the selected currency."
    )

    # Nisab = 85 grams of gold
    nisab_grams = models.DecimalField(
        max_digits=8, decimal_places=2,
        default=85.00,
        help_text="Nisab threshold in grams of gold (AAOIFI: 85g)."
    )
    nisab_value = models.DecimalField(
        max_digits=18, decimal_places=4,
        help_text="Nisab monetary value = nisab_grams × gold_price_per_gram."
    )

    # USD/MYR rate used (for conversion)
    usd_myr_rate = models.DecimalField(
        max_digits=10, decimal_places=4,
        null=True, blank=True,
        help_text="Exchange rate used for currency conversion."
    )

    # Portfolio snapshot
    portfolio_value = models.DecimalField(
        max_digits=18, decimal_places=4,
        help_text="Total portfolio market value at calculation time."
    )
    is_above_nisab = models.BooleanField(
        help_text="True if portfolio_value >= nisab_value."
    )

    # Zakat
    zakat_rate = models.DecimalField(
        max_digits=6, decimal_places=4,
        default=0.0250,
        help_text="Zakat rate (standard 2.5%)."
    )
    zakat_due = models.DecimalField(
        max_digits=18, decimal_places=4,
        help_text="Zakat due = portfolio_value × zakat_rate (if above nisab)."
    )

    class Meta:
        ordering = ["-calculated_at"]
        verbose_name = "Zakat Record"
        verbose_name_plural = "Zakat Records"

    def __str__(self):
        return f"Zakat {self.calculated_at.date()} — {self.currency} {float(self.zakat_due):,.2f}"
