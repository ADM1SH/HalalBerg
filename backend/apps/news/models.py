from django.db import models


class NewsItem(models.Model):
    SENTIMENT_CHOICES = [
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
    ]

    external_id = models.BigIntegerField(unique=True, null=True, blank=True)
    headline = models.CharField(max_length=200)
    summary = models.TextField()
    source = models.CharField(max_length=80)
    url = models.URLField(blank=True, default="")
    published_at = models.DateTimeField()
    related_symbols = models.CharField(max_length=120, blank=True, default="")
    sentiment = models.CharField(
        max_length=10, choices=SENTIMENT_CHOICES, default="neutral"
    )

    class Meta:
        ordering = ["-published_at"]

    def related_symbols_list(self):
        return [s.strip() for s in self.related_symbols.split(",") if s.strip()]

    def __str__(self):
        return self.headline
