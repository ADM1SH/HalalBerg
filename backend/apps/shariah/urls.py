from django.urls import path

from .views import ScreenerView, ShariahAssessmentDetailView

urlpatterns = [
    path("screener/", ScreenerView.as_view(), name="screener"),
    path(
        "assessments/<str:symbol>/",
        ShariahAssessmentDetailView.as_view(),
        name="assessment-detail",
    ),
]
