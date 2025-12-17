from django.utils.dateparse import parse_datetime
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Keyword, Mention
from .serializers import KeywordSerializer, MentionSerializer
from .services.hn_algolia import search_stories


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by("-created_at")
    serializer_class = KeywordSerializer

    @action(detail=True, methods=["POST"], url_path="sync_hn")
    def sync_hn(self, request, pk=None):
        keyword = self.get_object()

        hits_per_page = int(request.query_params.get("hitsPerPage", 20))
        page = int(request.query_params.get("page", 0))

        hits = search_stories(keyword.term, hits_per_page=hits_per_page, page=page)

        created = 0
        updated = 0

        for h in hits:
            external_id = str(h.get("objectID") or "")
            if not external_id:
                continue

            title = h.get("title") or h.get("story_title") or "(no title)"
            url = h.get("url") or h.get("story_url") or "https://news.ycombinator.com/"
            author = h.get("author") or ""
            points = h.get("points")
            published_at = parse_datetime(h.get("created_at")) if h.get("created_at") else None

            obj, was_created = Mention.objects.update_or_create(
                source="hn_algolia",
                external_id=external_id,
                defaults={
                    "keyword": keyword,
                    "title": title[:255],
                    "url": url,
                    "author": author[:120],
                    "points": points,
                    "published_at": published_at,
                },
            )

            if was_created:
                created += 1
            else:
                updated += 1

        return Response(
            {"keyword_id": keyword.id, "fetched": len(hits), "created": created, "updated": updated},
            status=status.HTTP_200_OK,
        )


class MentionViewSet(viewsets.ModelViewSet):
    queryset = Mention.objects.select_related("keyword").all().order_by("-created_at")
    serializer_class = MentionSerializer
