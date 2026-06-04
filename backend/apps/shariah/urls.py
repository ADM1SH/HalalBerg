"""Shariah app URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path("<str:ticker>/audit/", views.ShariahAuditView.as_view(), name="shariah-audit"),
    path("screener/", views.ShariahScreenerView.as_view(), name="shariah-screener"),
]
