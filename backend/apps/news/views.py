"""News views — stub placeholders. Full implementation in Phase 2."""
from rest_framework.views import APIView
from rest_framework.response import Response


class NewsListView(APIView):
    def get(self, request):
        return Response({"status": "not_implemented", "endpoint": "news"})


class NewsAISummariseView(APIView):
    def post(self, request, pk):
        return Response({"status": "not_implemented", "endpoint": f"news/{pk}/summarise"})
