from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Mention


@api_view(["GET"])
def mentions_daily(request):
    keyword_id = request.query_params.get("keyword_id")
    if not keyword_id:
        return Response({"detail": "keyword_id is required"}, status=400)

    days = int(request.query_params.get("days", 30))
    source = request.query_params.get("source")  # optional

    since = timezone.now() - timedelta(days=days)

    qs = Mention.objects.filter(keyword_id=keyword_id, created_at__gte=since)

    if source:
        qs = qs.filter(source=source)

    rows = (
        qs.annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    return Response(list(rows))
