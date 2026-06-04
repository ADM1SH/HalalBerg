"""
HalalBurg Terminal — Django Settings
Locally-running, single-user Shariah-compliant stock market terminal.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths & Env
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-key-change-in-production")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# ---------------------------------------------------------------------------
# Installed Apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    # HalalBurg apps
    "apps.market",
    "apps.fundamentals",
    "apps.shariah",
    "apps.portfolio",
    "apps.news",
    "apps.gold",
    "apps.ai_summary",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "halalburg.urls"
WSGI_APPLICATION = "halalburg.wsgi.application"

# ---------------------------------------------------------------------------
# Database — SQLite local cache
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "halalburg.db",
        # SQLite performance tuning for financial data
        "OPTIONS": {
            "timeout": 20,
        },
    }
}

# ---------------------------------------------------------------------------
# Static Files (not used in API-only backend, but required)
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        # Generous local rates — protects against accidental loops
        "anon": "600/min",
    },
}

# ---------------------------------------------------------------------------
# CORS — allow the Next.js dev server
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_ALL_ORIGINS = False

# ---------------------------------------------------------------------------
# External API Keys
# ---------------------------------------------------------------------------
FMP_API_KEY = os.getenv("FMP_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
GOLD_API_KEY = os.getenv("GOLD_API_KEY", "")
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "llama-3-8b-instruct")

# ---------------------------------------------------------------------------
# Currency
# ---------------------------------------------------------------------------
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "MYR")
FALLBACK_USD_MYR = float(os.getenv("FALLBACK_USD_MYR", "4.70"))

# ---------------------------------------------------------------------------
# Cache TTL settings (seconds)
# ---------------------------------------------------------------------------
PRICE_CACHE_TTL = 60          # Live quotes refresh every 60s
NEWS_CACHE_TTL = 300          # News refreshes every 5 minutes
GOLD_CACHE_TTL = 300          # Gold prices every 5 minutes
FUNDAMENTALS_CACHE_TTL = 86400  # Financial statements daily

# ---------------------------------------------------------------------------
# Shariah Screening Thresholds (AAOIFI Standard)
# ---------------------------------------------------------------------------
SHARIAH_DEBT_THRESHOLD = 0.33       # (Interest-bearing debt + cash) / total assets < 33%
SHARIAH_REVENUE_THRESHOLD = 0.05    # Non-compliant revenue / total revenue < 5%

# Sectors that auto-fail Shariah screening (qualitative exclusion)
SHARIAH_PROHIBITED_SECTORS = [
    "Banks",
    "Banking",
    "Diversified Financial Services",
    "Consumer Finance",
    "Capital Markets",
    "Thrifts & Mortgage Finance",
    "Beverages—Brewers",
    "Beverages—Wineries & Distilleries",
    "Tobacco",
    "Gambling",
    "Casinos & Gaming",
    "Aerospace & Defense",       # controversial — flag but not auto-exclude
    "Adult Entertainment",
]

# These sectors are hard-excluded (no override possible)
SHARIAH_HARD_EXCLUDED_SECTORS = [
    "Banks",
    "Banking",
    "Beverages—Brewers",
    "Beverages—Wineries & Distilleries",
    "Tobacco",
    "Gambling",
    "Casinos & Gaming",
    "Adult Entertainment",
]

# ---------------------------------------------------------------------------
# Internationalisation (minimal — local app)
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
