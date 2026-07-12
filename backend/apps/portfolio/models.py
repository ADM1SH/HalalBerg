from django.db import models

from apps.market.models import Quote


class PortfolioAccount(models.Model):
    """Single default account until auth lands (see project next-steps)."""

    cash_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    zakat_assessment_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Account #{self.pk}"


class Holding(models.Model):
    account = models.ForeignKey(
        PortfolioAccount, on_delete=models.CASCADE, related_name="holdings"
    )
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="+")
    quantity = models.DecimalField(max_digits=14, decimal_places=4)
    average_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} {self.quote.symbol}"
