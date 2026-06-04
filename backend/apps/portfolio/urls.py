"""Portfolio app URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path("holdings/", views.HoldingsView.as_view(), name="portfolio-holdings"),
    path("holdings/<int:pk>/", views.HoldingDetailView.as_view(), name="portfolio-holding-detail"),
    path("zakat/", views.ZakatView.as_view(), name="portfolio-zakat"),
    path("zakat/history/", views.ZakatHistoryView.as_view(), name="portfolio-zakat-history"),
    path("summary/", views.PortfolioSummaryView.as_view(), name="portfolio-summary"),
]
