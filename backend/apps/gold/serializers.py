from rest_framework import serializers

from .models import MetalSpot


class MetalSpotSerializer(serializers.ModelSerializer):
    spot_price_per_gram = serializers.FloatField(read_only=True)

    class Meta:
        model = MetalSpot
        fields = [
            "metal",
            "spot_price_per_ounce",
            "spot_price_per_gram",
            "change_percent",
            "as_of",
        ]
