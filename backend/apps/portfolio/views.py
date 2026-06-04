"""Portfolio views — stub placeholders. Full implementation in Phase 2."""
from rest_framework.views import APIView
from rest_framework.response import Response


class HoldingsView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "holdings"})

    def post(self, request):
        return Response({"status": "not_implemented"})


class HoldingDetailView(APIView):
    def get(self, request, pk):
        return Response({"status": "not_implemented"})

    def put(self, request, pk):
        return Response({"status": "not_implemented"})

    def delete(self, request, pk):
        return Response({"status": "not_implemented"})


class ZakatView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "zakat"})


class ZakatHistoryView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "zakat/history"})


class PortfolioSummaryView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "summary"})
