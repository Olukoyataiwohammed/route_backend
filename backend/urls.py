from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import home

urlpatterns = [
    path("", home, name="home"),

    path(
        "admin/",
        admin.site.urls,
    ),

    # JWT Authentication
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Apps
    path(
        "api/trips/",
        include("trips.urls"),
    ),

    path(
        "api/routing/",
        include("routing.urls"),
    ),

    path(
        "api/eld/",
        include("eld_logs.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )