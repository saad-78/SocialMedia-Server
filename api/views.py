# api/views.py
from rest_framework import viewsets
from .models import Keyword, Mention
from .serializers import KeywordSerializer, MentionSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by("-created_at")
    serializer_class = KeywordSerializer

class MentionViewSet(viewsets.ModelViewSet):
    queryset = Mention.objects.select_related("keyword").all().order_by("-created_at")
    serializer_class = MentionSerializer
