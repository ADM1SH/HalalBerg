from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Quote
from .serializers import QuoteSerializer
from .services import ensure_quotes_fresh


class QuoteListView(ListAPIView):
    serializer_class = QuoteSerializer

    def get_queryset(self):
        ensure_quotes_fresh()
        return Quote.objects.all()


class QuoteDetailView(RetrieveAPIView):
    serializer_class = QuoteSerializer
    lookup_field = "symbol"
    lookup_url_kwarg = "symbol"

    def get_queryset(self):
        ensure_quotes_fresh()
        return Quote.objects.all()
