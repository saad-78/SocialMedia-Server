from django.contrib import admin
from django.urls import path, include
from api.pages import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("dashboard/", dashboard),
]
