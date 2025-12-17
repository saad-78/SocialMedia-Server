from django.db import models

class Keyword(models.Model):
    term = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.term


class Mention(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="mentions")
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    source = models.CharField(max_length=80, default="manual")
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["keyword", "created_at"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self) -> str:
        return self.title
