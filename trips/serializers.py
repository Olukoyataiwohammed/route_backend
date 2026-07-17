from rest_framework import serializers

from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for Trip objects.
    """

    class Meta:
        model = Trip

        fields = [
            "id",
            "driver",
            "current_location",
            "pickup_location",
            "dropoff_location",
            "current_cycle_used",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "driver",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_current_cycle_used(self, value):
        """
        Validate the driver's current cycle hours.
        FMCSA limit is 70 hours / 8 days.
        """

        if value < 0:
            raise serializers.ValidationError(
                "Current cycle used cannot be negative."
            )

        if value > 70:
            raise serializers.ValidationError(
                "Current cycle used cannot exceed 70 hours."
            )

        return value

    def validate(self, attrs):
        """
        Prevent the user from entering the same
        location for pickup and dropoff.
        """

        pickup = attrs.get("pickup_location")
        dropoff = attrs.get("dropoff_location")

        if (
            pickup
            and dropoff
            and pickup.strip().lower() == dropoff.strip().lower()
        ):
            raise serializers.ValidationError(
                {
                    "dropoff_location": (
                        "Pickup and dropoff locations "
                        "cannot be the same."
                    )
                }
            )

        return attrs