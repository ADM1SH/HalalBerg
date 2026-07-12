from django.db import models


class MetalSpot(models.Model):
    METAL_CHOICES = [("gold", "Gold"), ("silver", "Silver")]

    metal = models.CharField(max_length=10, choices=METAL_CHOICES, unique=True)
    spot_price_per_ounce = models.DecimalField(max_digits=10, decimal_places=2)
    change_percent = models.FloatField(default=0)
    as_of = models.DateTimeField(auto_now=True)

    GRAMS_PER_OUNCE = 31.1035

    @property
    def spot_price_per_gram(self):
        return float(self.spot_price_per_ounce) / self.GRAMS_PER_OUNCE

    def __str__(self):
        return f"{self.metal}: {self.spot_price_per_ounce}"
