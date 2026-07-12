from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BlackScholesRequestSerializer, EfficientFrontierRequestSerializer
from .services import compute_efficient_frontier, price_black_scholes


class EfficientFrontierView(APIView):
    def post(self, request):
        serializer = EfficientFrontierRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = compute_efficient_frontier(serializer.validated_data["symbols"])
        return Response(result)


class BlackScholesView(APIView):
    def post(self, request):
        serializer = BlackScholesRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = price_black_scholes(**serializer.validated_data)
        return Response(result)
