from rest_framework import serializers

from .models import Holding


class HoldingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    symbol = serializers.CharField(source="quote.symbol")
    name = serializers.CharField(source="quote.name")
    current_price = serializers.DecimalField(
        source="quote.price", max_digits=12, decimal_places=2
    )
    is_shariah_compliant = serializers.BooleanField(source="quote.is_shariah_compliant")
    market_value = serializers.SerializerMethodField()
    unrealized_pnl = serializers.SerializerMethodField()
    unrealized_pnl_percent = serializers.SerializerMethodField()

    class Meta:
        model = Holding
        fields = [
            "id",
            "symbol",
            "name",
            "quantity",
            "average_cost",
            "current_price",
            "market_value",
            "unrealized_pnl",
            "unrealized_pnl_percent",
            "is_shariah_compliant",
        ]

    def get_market_value(self, obj):
        return round(float(obj.quantity) * float(obj.quote.price), 2)

    def get_unrealized_pnl(self, obj):
        cost_basis = float(obj.quantity) * float(obj.average_cost)
        return round(self.get_market_value(obj) - cost_basis, 2)

    def get_unrealized_pnl_percent(self, obj):
        cost_basis = float(obj.quantity) * float(obj.average_cost)
        if cost_basis == 0:
            return 0.0
        return round((self.get_unrealized_pnl(obj) / cost_basis) * 100, 2)
