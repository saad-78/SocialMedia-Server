import uuid
from django.db import models

def gen_external_id() -> str:
    return uuid.uuid4().hex


class Keyword(models.Model):
    term = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.term


class Mention(models.Model):
    keyword = models.ForeignKey("Keyword", on_delete=models.CASCADE, related_name="mentions")
    external_id = models.CharField(max_length=40, default=gen_external_id)  # Algolia objectID fits here
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    source = models.CharField(max_length=80, default="manual")
    author = models.CharField(max_length=120, blank=True, default="")
    points = models.IntegerField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source", "external_id"], name="uniq_source_external_id")
        ]
        indexes = [
            models.Index(fields=["keyword", "created_at"]),
            models.Index(fields=["source"]),
        ]


    def __str__(self) -> str:
        return self.title
