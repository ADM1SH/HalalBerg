"""Market app URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path("quote/<str:ticker>/", views.QuoteView.as_view(), name="market-quote"),
    path("history/<str:ticker>/", views.PriceHistoryView.as_view(), name="market-history"),
    path("search/", views.TickerSearchView.as_view(), name="market-search"),
    path("tape/", views.TickerTapeView.as_view(), name="market-tape"),
    path("watchlist/", views.WatchlistView.as_view(), name="market-watchlist"),
    path("watchlist/<int:pk>/", views.WatchlistDetailView.as_view(), name="market-watchlist-detail"),
]
