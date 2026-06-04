"""Gold app URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path("spot/", views.GoldSpotView.as_view(), name="gold-spot"),
    path("nisab/", views.NisabView.as_view(), name="gold-nisab"),
]
