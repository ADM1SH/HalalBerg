from rest_framework import serializers

from .models import ShariahAssessment


class ShariahAssessmentSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="quote.symbol")

    class Meta:
        model = ShariahAssessment
        fields = [
            "symbol",
            "status",
            "debt_to_market_cap",
            "liquid_assets_ratio",
            "interest_income_ratio",
            "non_compliant_income_ratio",
            "notes",
        ]


class ScreenerRowSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="quote.symbol")
    name = serializers.CharField(source="quote.name")
    sector = serializers.CharField(source="quote.sector")
    price = serializers.DecimalField(
        source="quote.price", max_digits=12, decimal_places=2
    )
    market_cap = serializers.IntegerField(source="quote.market_cap")

    class Meta:
        model = ShariahAssessment
        fields = [
            "symbol",
            "name",
            "sector",
            "price",
            "market_cap",
            "status",
            "debt_to_market_cap",
            "non_compliant_income_ratio",
            "notes",
        ]
