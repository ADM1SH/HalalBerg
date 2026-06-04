"""Fundamentals views — stub placeholders. Full implementation in Phase 2."""
from rest_framework.views import APIView
from rest_framework.response import Response


class IncomeStatementView(APIView):
    def get(self, request, ticker):
        return Response({"status": "not_implemented", "endpoint": f"{ticker}/income"})


class BalanceSheetView(APIView):
    def get(self, request, ticker):
        return Response({"status": "not_implemented", "endpoint": f"{ticker}/balance"})


class CashFlowView(APIView):
    def get(self, request, ticker):
        return Response({"status": "not_implemented", "endpoint": f"{ticker}/cashflow"})
