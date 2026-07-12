from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import ShariahAssessment
from .serializers import ScreenerRowSerializer, ShariahAssessmentSerializer
from .services import ensure_assessments_fresh


class ShariahAssessmentDetailView(RetrieveAPIView):
    serializer_class = ShariahAssessmentSerializer
    lookup_field = "quote__symbol"
    lookup_url_kwarg = "symbol"

    def get_queryset(self):
        ensure_assessments_fresh()
        return ShariahAssessment.objects.select_related("quote")


class ScreenerView(ListAPIView):
    serializer_class = ScreenerRowSerializer

    def get_queryset(self):
        ensure_assessments_fresh()
        qs = ShariahAssessment.objects.select_related("quote")

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(quote__symbol__icontains=search) | Q(quote__name__icontains=search)
            )

        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)

        sector = self.request.query_params.get("sector")
        if sector:
            qs = qs.filter(quote__sector=sector)

        return qs.order_by("quote__symbol")
