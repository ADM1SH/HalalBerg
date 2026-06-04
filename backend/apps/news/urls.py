"""News app URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.NewsListView.as_view(), name="news-list"),
    path("<int:pk>/summarise/", views.NewsAISummariseView.as_view(), name="news-summarise"),
]
