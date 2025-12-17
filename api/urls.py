from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KeywordViewSet, MentionViewSet
from .reports import mentions_daily

router = DefaultRouter()
router.register(r"keywords", KeywordViewSet, basename="keyword")
router.register(r"mentions", MentionViewSet, basename="mention")

urlpatterns = [
    path("", include(router.urls)),
    path("reports/mentions_daily/", mentions_daily),
]
