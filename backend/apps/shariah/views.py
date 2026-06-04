"""Shariah views — stub placeholders. Full implementation in Phase 2."""
from rest_framework.views import APIView
from rest_framework.response import Response


class ShariahAuditView(APIView):
    def get(self, request, ticker):
        return Response({"status": "not_implemented", "endpoint": f"{ticker}/audit"})


class ShariahScreenerView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "screener"})
