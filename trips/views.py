from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Trip
from .serializers import TripSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def trip_list_create(request):
    """
    List all trips for the logged-in driver
    or create a new trip.
    """

    if request.method == "GET":
        trips = Trip.objects.filter(
            driver=request.user
        )

        serializer = TripSerializer(
            trips,
            many=True,
        )

        return Response(
            {
                "success": True,
                "count": trips.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    serializer = TripSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save(
            driver=request.user
        )

        return Response(
            {
                "success": True,
                "message": "Trip created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {
            "success": False,
            "errors": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def trip_detail(request, pk):
    """
    Retrieve, update, or delete one of the
    logged-in driver's trips.
    """

    trip = get_object_or_404(
        Trip,
        pk=pk,
        driver=request.user,
    )

    if request.method == "GET":
        serializer = TripSerializer(trip)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    if request.method == "PUT":
        serializer = TripSerializer(
            trip,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Trip updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "PATCH":
        serializer = TripSerializer(
            trip,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Trip updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    trip.delete()

    return Response(
        {
            "success": True,
            "message": "Trip deleted successfully.",
        },
        status=status.HTTP_204_NO_CONTENT,
    )