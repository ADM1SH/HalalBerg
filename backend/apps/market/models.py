from django.db import models


class Quote(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=120)
    sector = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    change = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    change_percent = models.FloatField(default=0)
    volume = models.BigIntegerField(default=0)
    market_cap = models.BigIntegerField(default=0)
    is_shariah_compliant = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return self.symbol
