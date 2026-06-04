"""Gold views — stub placeholders. Full implementation in Phase 2."""
from rest_framework.views import APIView
from rest_framework.response import Response


class GoldSpotView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "gold/spot"})


class NisabView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "gold/nisab"})
