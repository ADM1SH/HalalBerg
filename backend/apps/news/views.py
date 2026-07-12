from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NewsItem
from .risk import compute_risk_signal
from .serializers import NewsItemSerializer
from .services import ensure_news_fresh


class NewsFeedView(ListAPIView):
    serializer_class = NewsItemSerializer

    def get_queryset(self):
        ensure_news_fresh()
        return NewsItem.objects.all()[:30]


class RiskSignalView(APIView):
    def get(self, request):
        return Response(compute_risk_signal())
