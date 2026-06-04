"""AI Summary views — stub placeholders. Full implementation in Phase 2."""
from rest_framework.views import APIView
from rest_framework.response import Response


class AISummariseView(APIView):
    def post(self, request):
        return Response({"status": "not_implemented", "endpoint": "ai/summarise"})


class LMStudioStatusView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "ai/status"})
