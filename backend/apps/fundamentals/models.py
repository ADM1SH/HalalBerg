"""
Fundamentals app — caches 5-10 years of financial statements from FMP.
Data source: Financial Modeling Prep free tier API.
"""

from django.db import models
from apps.market.models import Ticker


class IncomeStatement(models.Model):
    """
    Annual and quarterly income statements from FMP.
    Interest expense is key for Shariah revenue screening.
    """
    PERIOD_ANNUAL = "annual"
    PERIOD_QUARTERLY = "quarterly"
    PERIOD_CHOICES = [
        (PERIOD_ANNUAL, "Annual"),
        (PERIOD_QUARTERLY, "Quarterly"),
    ]

    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name="income_statements")
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    fiscal_year = models.IntegerField()
    fiscal_quarter = models.IntegerField(null=True, blank=True)   # 1-4, null for annual
    report_date = models.DateField(null=True, blank=True)

    # Revenue
    revenue = models.BigIntegerField(null=True, blank=True)
    cost_of_revenue = models.BigIntegerField(null=True, blank=True)
    gross_profit = models.BigIntegerField(null=True, blank=True)
    gross_profit_margin = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    # Operating
    operating_expenses = models.BigIntegerField(null=True, blank=True)
    operating_income = models.BigIntegerField(null=True, blank=True)
    operating_margin = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    ebitda = models.BigIntegerField(null=True, blank=True)

    # Below the line
    interest_expense = models.BigIntegerField(null=True, blank=True)  # KEY for Shariah audit
    interest_income = models.BigIntegerField(null=True, blank=True)   # KEY for Shariah revenue screen
    pretax_income = models.BigIntegerField(null=True, blank=True)
    income_tax_expense = models.BigIntegerField(null=True, blank=True)
    net_income = models.BigIntegerField(null=True, blank=True)
    net_profit_margin = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    # Per share
    eps = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    eps_diluted = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    weighted_avg_shares = models.BigIntegerField(null=True, blank=True)

    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("ticker", "period", "fiscal_year", "fiscal_quarter")
        ordering = ["-fiscal_year", "-fiscal_quarter"]
        verbose_name = "Income Statement"

    def __str__(self):
        period_str = f"Q{self.fiscal_quarter}" if self.fiscal_quarter else "Annual"
        return f"{self.ticker.symbol} IS {self.fiscal_year} {period_str}"


class BalanceSheet(models.Model):
    """
    Annual and quarterly balance sheets from FMP.
    Total debt and total assets are the core inputs for Shariah debt ratio.
    Formula: (interest_bearing_debt + cash) / total_assets < 33%
    """
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name="balance_sheets")
    period = models.CharField(max_length=10, choices=IncomeStatement.PERIOD_CHOICES)
    fiscal_year = models.IntegerField()
    fiscal_quarter = models.IntegerField(null=True, blank=True)
    report_date = models.DateField(null=True, blank=True)

    # Assets
    total_assets = models.BigIntegerField(null=True, blank=True)              # KEY for Shariah audit
    cash_and_equivalents = models.BigIntegerField(null=True, blank=True)      # KEY for Shariah audit
    short_term_investments = models.BigIntegerField(null=True, blank=True)
    accounts_receivable = models.BigIntegerField(null=True, blank=True)
    inventory = models.BigIntegerField(null=True, blank=True)
    total_current_assets = models.BigIntegerField(null=True, blank=True)
    net_ppe = models.BigIntegerField(null=True, blank=True)                   # Net PP&E
    goodwill = models.BigIntegerField(null=True, blank=True)
    intangible_assets = models.BigIntegerField(null=True, blank=True)
    total_non_current_assets = models.BigIntegerField(null=True, blank=True)

    # Liabilities
    total_liabilities = models.BigIntegerField(null=True, blank=True)
    accounts_payable = models.BigIntegerField(null=True, blank=True)
    short_term_debt = models.BigIntegerField(null=True, blank=True)           # Interest-bearing ST debt
    total_current_liabilities = models.BigIntegerField(null=True, blank=True)
    long_term_debt = models.BigIntegerField(null=True, blank=True)            # KEY for Shariah audit
    total_non_current_liabilities = models.BigIntegerField(null=True, blank=True)
    total_debt = models.BigIntegerField(null=True, blank=True)                # ST + LT interest-bearing debt

    # Equity
    total_equity = models.BigIntegerField(null=True, blank=True)
    retained_earnings = models.BigIntegerField(null=True, blank=True)
    common_stock = models.BigIntegerField(null=True, blank=True)

    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("ticker", "period", "fiscal_year", "fiscal_quarter")
        ordering = ["-fiscal_year", "-fiscal_quarter"]
        verbose_name = "Balance Sheet"

    def __str__(self):
        period_str = f"Q{self.fiscal_quarter}" if self.fiscal_quarter else "Annual"
        return f"{self.ticker.symbol} BS {self.fiscal_year} {period_str}"

    @property
    def shariah_debt_ratio(self):
        """
        AAOIFI debt screening ratio:
        (interest-bearing debt + cash & equivalents) / total assets
        Returns float or None if data unavailable.
        """
        if not self.total_assets or self.total_assets == 0:
            return None
        debt = self.total_debt or 0
        cash = self.cash_and_equivalents or 0
        return (debt + cash) / self.total_assets


class CashFlowStatement(models.Model):
    """
    Cash flow statements from FMP.
    Free cash flow is key for portfolio valuation and Zakat calculation.
    """
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name="cash_flows")
    period = models.CharField(max_length=10, choices=IncomeStatement.PERIOD_CHOICES)
    fiscal_year = models.IntegerField()
    fiscal_quarter = models.IntegerField(null=True, blank=True)
    report_date = models.DateField(null=True, blank=True)

    # Operating
    net_income = models.BigIntegerField(null=True, blank=True)
    depreciation_amortization = models.BigIntegerField(null=True, blank=True)
    stock_based_compensation = models.BigIntegerField(null=True, blank=True)
    changes_in_working_capital = models.BigIntegerField(null=True, blank=True)
    operating_cash_flow = models.BigIntegerField(null=True, blank=True)

    # Investing
    capex = models.BigIntegerField(null=True, blank=True)
    acquisitions = models.BigIntegerField(null=True, blank=True)
    investing_cash_flow = models.BigIntegerField(null=True, blank=True)

    # Financing
    debt_repayment = models.BigIntegerField(null=True, blank=True)
    dividends_paid = models.BigIntegerField(null=True, blank=True)
    share_buybacks = models.BigIntegerField(null=True, blank=True)
    financing_cash_flow = models.BigIntegerField(null=True, blank=True)

    # Summary
    free_cash_flow = models.BigIntegerField(null=True, blank=True)
    net_change_in_cash = models.BigIntegerField(null=True, blank=True)

    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("ticker", "period", "fiscal_year", "fiscal_quarter")
        ordering = ["-fiscal_year", "-fiscal_quarter"]
        verbose_name = "Cash Flow Statement"

    def __str__(self):
        period_str = f"Q{self.fiscal_quarter}" if self.fiscal_quarter else "Annual"
        return f"{self.ticker.symbol} CF {self.fiscal_year} {period_str}"
