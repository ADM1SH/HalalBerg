from rest_framework import serializers


class EfficientFrontierRequestSerializer(serializers.Serializer):
    symbols = serializers.ListField(
        child=serializers.CharField(max_length=10), min_length=2, max_length=15
    )


class BlackScholesRequestSerializer(serializers.Serializer):
    spot_price = serializers.FloatField(min_value=0.01)
    strike_price = serializers.FloatField(min_value=0.01)
    time_to_expiry_years = serializers.FloatField(min_value=0.001, max_value=30)
    risk_free_rate = serializers.FloatField(min_value=-0.1, max_value=1)
    volatility = serializers.FloatField(min_value=0.001, max_value=5)
    option_type = serializers.ChoiceField(choices=["call", "put"])
