from django.db import models

from apps.market.models import Quote


class ShariahAssessment(models.Model):
    STATUS_CHOICES = [
        ("compliant", "Compliant"),
        ("non_compliant", "Non-compliant"),
        ("questionable", "Questionable"),
    ]

    quote = models.OneToOneField(
        Quote, on_delete=models.CASCADE, related_name="assessment"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    debt_to_market_cap = models.FloatField(default=0)
    liquid_assets_ratio = models.FloatField(default=0)
    interest_income_ratio = models.FloatField(default=0)
    non_compliant_income_ratio = models.FloatField(default=0)
    notes = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quote.symbol}: {self.status}"
