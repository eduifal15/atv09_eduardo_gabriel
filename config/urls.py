"""URL configuration for config project."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Todas as outras URLs são tratadas pelo app portal.
    path("", include("portal.urls")),
]
