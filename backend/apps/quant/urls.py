from django.urls import path

from .views import BlackScholesView, EfficientFrontierView

urlpatterns = [
    path(
        "efficient-frontier/",
        EfficientFrontierView.as_view(),
        name="efficient-frontier",
    ),
    path("black-scholes/", BlackScholesView.as_view(), name="black-scholes"),
]
