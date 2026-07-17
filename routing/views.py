from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from trips.models import Trip
from .services import RouteService


@api_view(["POST"])
def generate_route(request, pk):
    """
    Generate route information for a trip.
    """

    trip = get_object_or_404(Trip, pk=pk)

    route_service = RouteService()

    route = route_service.calculate_route(
        current_location=trip.current_location,
        pickup_location=trip.pickup_location,
        dropoff_location=trip.dropoff_location,
    )

    return Response(
        {
            "success": True,
            "message": "Route generated successfully.",
            "trip_id": str(trip.id),
            "route": route,
        },
        status=status.HTTP_200_OK,
    )
