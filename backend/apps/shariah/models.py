"""
Shariah app — audit engine and screening models.
Implements AAOIFI + Securities Commission Malaysia (SC) dual-standard screening.

Key thresholds (from settings.py):
  SHARIAH_DEBT_THRESHOLD = 0.33    → (debt + cash) / total_assets < 33%
  SHARIAH_REVENUE_THRESHOLD = 0.05 → non-halal income / total_revenue < 5%
"""

from django.db import models
from apps.market.models import Ticker


class ShariahAudit(models.Model):
    """
    Shariah compliance audit result for a ticker.
    Computed by apps/shariah/services.py using FMP balance sheet data.
    Stored to avoid recomputing on every request.
    """
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    DOUBTFUL = "DOUBTFUL"
    PENDING = "PENDING"

    STATUS_CHOICES = [
        (COMPLIANT, "Compliant"),
        (NON_COMPLIANT, "Non-Compliant"),
        (DOUBTFUL, "Doubtful"),
        (PENDING, "Pending Review"),
    ]

    ticker = models.OneToOneField(
        Ticker,
        on_delete=models.CASCADE,
        related_name="shariah_audit",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    # --- Quantitative screening (AAOIFI Standard) ---
    # Ratio 1: (interest-bearing debt + cash) / total assets
    debt_ratio = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True,
        help_text="(total_debt + cash) / total_assets. Threshold: < 33%"
    )
    debt_ratio_pass = models.BooleanField(null=True, blank=True)

    # Ratio 2: interest income / total revenue (non-halal income proxy)
    revenue_ratio = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True,
        help_text="interest_income / total_revenue. Threshold: < 5%"
    )
    revenue_ratio_pass = models.BooleanField(null=True, blank=True)

    # Ratio 3: accounts_receivable / (market_cap + total_debt + total_equity)
    # Used by AAOIFI; secondary check
    receivables_ratio = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True,
        help_text="accounts_receivable / total_assets. Threshold: < 70%"
    )
    receivables_ratio_pass = models.BooleanField(null=True, blank=True)

    # --- Qualitative screening ---
    business_activity_ok = models.BooleanField(
        default=True,
        help_text="False if core business is haram (alcohol, gambling, riba, etc.)"
    )
    excluded_sector = models.BooleanField(
        default=False,
        help_text="True if sector is on the hard-excluded list (auto-fail)."
    )

    # --- Standard-specific pass flags ---
    aaoifi_pass = models.BooleanField(
        null=True, blank=True,
        help_text="AAOIFI global Shariah standard (used by GCC, Malaysia, globally)."
    )
    sc_malaysia_pass = models.BooleanField(
        null=True, blank=True,
        help_text="Securities Commission Malaysia Shariah Advisory Council standard."
    )

    # --- Fiscal year of the underlying balance sheet data ---
    data_fiscal_year = models.IntegerField(null=True, blank=True)

    # --- AI-generated qualitative summary (optional) ---
    audit_notes = models.TextField(
        blank=True,
        help_text="Human-readable audit summary including qualitative findings."
    )

    # --- Dividend purification ---
    purification_rate = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True,
        help_text="Fraction of each dividend to purify (donate). Equals revenue_ratio."
    )

    screened_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Shariah Audit"
        verbose_name_plural = "Shariah Audits"

    def __str__(self):
        return f"{self.ticker.symbol} → {self.status}"

    @property
    def is_compliant(self):
        return self.status == self.COMPLIANT

    @property
    def debt_ratio_pct(self):
        """Returns debt ratio as a percentage string for display."""
        if self.debt_ratio is None:
            return "N/A"
        return f"{float(self.debt_ratio) * 100:.1f}%"

    @property
    def revenue_ratio_pct(self):
        """Returns revenue ratio as a percentage string for display."""
        if self.revenue_ratio is None:
            return "N/A"
        return f"{float(self.revenue_ratio) * 100:.1f}%"


class ScreenerCache(models.Model):
    """
    Pre-computed screener results for fast filtered queries.
    Rebuilt nightly by a background task.
    """
    ticker = models.OneToOneField(
        Ticker,
        on_delete=models.CASCADE,
        related_name="screener_cache",
    )
    shariah_status = models.CharField(max_length=20, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    market_cap_category = models.CharField(
        max_length=20, blank=True,
        help_text="mega/large/mid/small/micro — computed from market_cap."
    )
    last_price = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    pct_change = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    exchange = models.CharField(max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Screener Cache"
        verbose_name_plural = "Screener Caches"
        ordering = ["-market_cap"]

    def __str__(self):
        return f"{self.ticker.symbol} [{self.shariah_status}]"
