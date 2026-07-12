"""
URL configuration for halalburg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def api_root(request):
    return JsonResponse({
        "service": "HalalBurg Terminal API",
        "frontend": "http://localhost:3000",
        "endpoints": [
            "/admin/",
            "/api/market/quotes/",
            "/api/market/quotes/<symbol>/",
            "/api/portfolio/summary/",
            "/api/gold/spot/",
            "/api/gold/nisab/",
            "/api/shariah/screener/",
            "/api/shariah/assessments/<symbol>/",
            "/api/quant/efficient-frontier/",
            "/api/quant/black-scholes/",
            "/api/news/feed/",
        ],
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/market/', include('apps.market.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/gold/', include('apps.gold.urls')),
    path('api/shariah/', include('apps.shariah.urls')),
    path('api/quant/', include('apps.quant.urls')),
    path('api/news/', include('apps.news.urls')),
]
