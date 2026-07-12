from django.urls import path

from .views import NewsFeedView, RiskSignalView

urlpatterns = [
    path("feed/", NewsFeedView.as_view(), name="news-feed"),
    path("risk/", RiskSignalView.as_view(), name="news-risk"),
]
