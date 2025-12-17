from rest_framework import serializers
from .models import Keyword, Mention

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "term", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]

class MentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mention
        fields = [
            "id",
            "keyword",
            "external_id",
            "title",
            "url",
            "source",
            "author",
            "points",
            "published_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

