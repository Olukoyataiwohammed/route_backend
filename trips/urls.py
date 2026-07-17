from django.urls import path
from . import views

urlpatterns = [
    path("", views.trip_list_create, name="trip-list-create"),
    path("<uuid:pk>/", views.trip_detail, name="trip-detail"),
]

