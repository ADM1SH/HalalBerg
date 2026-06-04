"""Fundamentals app URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path("<str:ticker>/income/", views.IncomeStatementView.as_view(), name="fundamentals-income"),
    path("<str:ticker>/balance/", views.BalanceSheetView.as_view(), name="fundamentals-balance"),
    path("<str:ticker>/cashflow/", views.CashFlowView.as_view(), name="fundamentals-cashflow"),
]
