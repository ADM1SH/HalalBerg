"""
Market app views — stub placeholders.
Full implementation in Phase 2.
"""

from rest_framework.views import APIView
from rest_framework.response import Response


class QuoteView(APIView):
    def get(self, request, ticker):
        return Response({"status": "not_implemented", "endpoint": f"quote/{ticker}"})


class PriceHistoryView(APIView):
    def get(self, request, ticker):
        return Response({"status": "not_implemented", "endpoint": f"history/{ticker}"})


class TickerSearchView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "search"})


class TickerTapeView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "tape"})


class WatchlistView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "watchlist"})

    def post(self, request):
        return Response({"status": "not_implemented"})


class WatchlistDetailView(APIView):
    def delete(self, request, pk):
        return Response({"status": "not_implemented"})
