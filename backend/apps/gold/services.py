import logging

from django.utils import timezone

from apps.market.providers import goldapi_spot

from .models import MetalSpot

logger = logging.getLogger(__name__)

METAL_STALE_SECONDS = 180
METAL_CODES = {"gold": "XAU", "silver": "XAG"}


def spot_is_stale() -> bool:
    latest = MetalSpot.objects.order_by("-as_of").values_list("as_of", flat=True).first()
    if latest is None:
        return True
    return (timezone.now() - latest).total_seconds() > METAL_STALE_SECONDS


def refresh_metal_spot() -> None:
    for metal, code in METAL_CODES.items():
        try:
            data = goldapi_spot(code)
        except Exception:
            logger.exception("gold refresh failed for %s", metal)
            continue

        MetalSpot.objects.update_or_create(
            metal=metal,
            defaults={
                "spot_price_per_ounce": data.get("price") or 0,
                "change_percent": data.get("chp") or 0,
            },
        )


def ensure_spot_fresh() -> None:
    if spot_is_stale():
        refresh_metal_spot()
