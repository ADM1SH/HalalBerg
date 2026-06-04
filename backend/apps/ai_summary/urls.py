"""AI Summary app URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path("summarise/", views.AISummariseView.as_view(), name="ai-summarise"),
    path("status/", views.LMStudioStatusView.as_view(), name="ai-lmstudio-status"),
]
