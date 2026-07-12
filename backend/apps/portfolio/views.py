from rest_framework.response import Response
from rest_framework.views import APIView

from apps.gold.models import MetalSpot
from apps.gold.services import ensure_spot_fresh
from apps.gold.views import SILVER_NISAB_GRAMS
from apps.market.services import ensure_quotes_fresh

from .models import PortfolioAccount
from .serializers import HoldingSerializer

ZAKAT_RATE = 0.025


class PortfolioSummaryView(APIView):
    def get(self, request):
        ensure_quotes_fresh()
        ensure_spot_fresh()
        account = PortfolioAccount.objects.prefetch_related(
            "holdings__quote"
        ).first()

        if account is None:
            return Response(
                {
                    "total_market_value": 0,
                    "total_cost_basis": 0,
                    "total_unrealized_pnl": 0,
                    "total_unrealized_pnl_percent": 0,
                    "cash_balance": 0,
                    "zakat_due": 0,
                    "zakat_assessment_date": None,
                    "holdings": [],
                }
            )

        holdings = list(account.holdings.all())
        holdings_data = HoldingSerializer(holdings, many=True).data

        total_market_value = sum(h["market_value"] for h in holdings_data)
        total_cost_basis = sum(
            float(h.quantity) * float(h.average_cost) for h in holdings
        )
        total_unrealized_pnl = round(total_market_value - total_cost_basis, 2)
        total_unrealized_pnl_percent = (
            round((total_unrealized_pnl / total_cost_basis) * 100, 2)
            if total_cost_basis
            else 0.0
        )

        total_wealth = total_market_value + float(account.cash_balance)

        silver = MetalSpot.objects.filter(metal="silver").first()
        nisab_value = (
            SILVER_NISAB_GRAMS * silver.spot_price_per_gram if silver else 0
        )
        zakat_due = round(total_wealth * ZAKAT_RATE, 2) if total_wealth >= nisab_value else 0

        return Response(
            {
                "total_market_value": round(total_market_value, 2),
                "total_cost_basis": round(total_cost_basis, 2),
                "total_unrealized_pnl": total_unrealized_pnl,
                "total_unrealized_pnl_percent": total_unrealized_pnl_percent,
                "cash_balance": float(account.cash_balance),
                "zakat_due": zakat_due,
                "zakat_assessment_date": account.zakat_assessment_date,
                "holdings": holdings_data,
            }
        )
