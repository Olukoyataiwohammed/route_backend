from rest_framework import serializers


class RouteRequestSerializer(serializers.Serializer):
    """
    Validate the data required to
    generate a route.
    """

    current_location = serializers.CharField(max_length=255)
    pickup_location = serializers.CharField(max_length=255)
    dropoff_location = serializers.CharField(max_length=255)


class FuelStopSerializer(serializers.Serializer):
    """
    Represents a fuel stop.
    """

    stop_number = serializers.IntegerField()
    mile_marker = serializers.FloatField()
    reason = serializers.CharField()


class RouteResponseSerializer(serializers.Serializer):
    """
    Route information returned
    to the frontend.
    """

    current_location = serializers.CharField()
    pickup_location = serializers.CharField()
    dropoff_location = serializers.CharField()

    distance_miles = serializers.FloatField()

    driving_time_hours = serializers.FloatField()

    fuel_stops = FuelStopSerializer(many=True)

    coordinates = serializers.ListField(
        child=serializers.DictField()
    )

    directions = serializers.ListField(
        child=serializers.DictField()
    )