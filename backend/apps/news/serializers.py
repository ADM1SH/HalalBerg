from rest_framework import serializers

from .models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    related_symbols = serializers.SerializerMethodField()

    class Meta:
        model = NewsItem
        fields = [
            "id",
            "headline",
            "summary",
            "source",
            "url",
            "published_at",
            "related_symbols",
            "sentiment",
        ]

    def get_related_symbols(self, obj):
        return obj.related_symbols_list()
