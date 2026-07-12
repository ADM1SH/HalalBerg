from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MetalSpot
from .serializers import MetalSpotSerializer
from .services import ensure_spot_fresh

GOLD_NISAB_GRAMS = 85
SILVER_NISAB_GRAMS = 595


class MetalSpotListView(ListAPIView):
    serializer_class = MetalSpotSerializer

    def get_queryset(self):
        ensure_spot_fresh()
        return MetalSpot.objects.all()


class NisabView(APIView):
    def get(self, request):
        ensure_spot_fresh()
        gold = MetalSpot.objects.filter(metal="gold").first()
        silver = MetalSpot.objects.filter(metal="silver").first()

        gold_nisab_value = (
            GOLD_NISAB_GRAMS * gold.spot_price_per_gram if gold else 0
        )
        silver_nisab_value = (
            SILVER_NISAB_GRAMS * silver.spot_price_per_gram if silver else 0
        )

        # Silver standard is conventionally used as the applicable (lower,
        # more inclusive) nisab threshold for mixed cash/investment wealth.
        applicable = (
            silver_nisab_value if silver_nisab_value > 0 else gold_nisab_value
        )

        return Response(
            {
                "gold_nisab_grams": GOLD_NISAB_GRAMS,
                "silver_nisab_grams": SILVER_NISAB_GRAMS,
                "gold_nisab_value": round(gold_nisab_value, 2),
                "silver_nisab_value": round(silver_nisab_value, 2),
                "applicable_nisab_value": round(applicable, 2),
                "as_of": timezone.now(),
            }
        )
