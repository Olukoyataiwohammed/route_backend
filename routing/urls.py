from django.urls import path
from . import views

urlpatterns = [
    path(
        "<uuid:pk>/",
        views.generate_route,
        name="generate-route",
    ),
]