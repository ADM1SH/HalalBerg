from django.urls import path

from .views import MetalSpotListView, NisabView

urlpatterns = [
    path("spot/", MetalSpotListView.as_view(), name="metal-spot"),
    path("nisab/", NisabView.as_view(), name="nisab"),
]
