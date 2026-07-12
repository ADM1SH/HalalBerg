from rest_framework import serializers

from .models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = [
            "symbol",
            "name",
            "sector",
            "price",
            "change",
            "change_percent",
            "volume",
            "market_cap",
            "is_shariah_compliant",
        ]
