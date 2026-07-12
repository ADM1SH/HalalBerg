from django.urls import path

from .views import QuoteDetailView, QuoteListView

urlpatterns = [
    path("quotes/", QuoteListView.as_view(), name="quote-list"),
    path("quotes/<str:symbol>/", QuoteDetailView.as_view(), name="quote-detail"),
]
