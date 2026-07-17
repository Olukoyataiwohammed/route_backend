from rest_framework import serializers

from .models import ELDLog


class ELDLogSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving
    Electronic Logging Device (ELD) logs.

    Validates FMCSA Hours of Service (HOS)
    requirements.
    """

    class Meta:
        model = ELDLog

        fields = [
            "id",
            "driver",
            "driving_hours",
            "on_duty_hours",
            "cycle_hours_used",
            "cycle_type",
            "adverse_conditions",
            "remaining_driving_hours",
            "remaining_on_duty_hours",
            "remaining_cycle_hours",
            "break_required",
            "off_duty_reset_required",
            "hos_violations",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "driver",
            "remaining_driving_hours",
            "remaining_on_duty_hours",
            "remaining_cycle_hours",
            "break_required",
            "off_duty_reset_required",
            "hos_violations",
            "created_at",
        ]

    def validate_driving_hours(self, value):
        """
        Validate daily driving hours.
        """

        if value < 0:
            raise serializers.ValidationError(
                "Driving hours cannot be negative."
            )

        return value

    def validate_on_duty_hours(self, value):
        """
        Validate on-duty hours.
        """

        if value < 0:
            raise serializers.ValidationError(
                "On-duty hours cannot be negative."
            )

        return value

    def validate_cycle_hours_used(self, value):
        """
        Validate cycle hours.
        """

        if value < 0:
            raise serializers.ValidationError(
                "Cycle hours cannot be negative."
            )

        return value

    def validate_cycle_type(self, value):
        """
        Validate FMCSA cycle type.
        """

        if value not in ["60", "70"]:
            raise serializers.ValidationError(
                "Cycle type must be '60' or '70'."
            )

        return value

    def validate(self, attrs):
        """
        Cross-field FMCSA HOS validation.
        """

        driving = attrs.get(
            "driving_hours",
            0
        )

        duty = attrs.get(
            "on_duty_hours",
            0
        )

        cycle = attrs.get(
            "cycle_type"
        )

        used = attrs.get(
            "cycle_hours_used",
            0
        )

        # Driving hours cannot exceed total on-duty hours
        if driving > duty:
            raise serializers.ValidationError(
                {
                    "driving_hours": (
                        "Driving hours cannot exceed "
                        "on-duty hours."
                    )
                }
            )

        # FMCSA 11-hour driving limit
        if driving > 11:
            raise serializers.ValidationError(
                {
                    "driving_hours": (
                        "Driving hours cannot exceed "
                        "11 hours per duty period."
                    )
                }
            )

        # FMCSA 14-hour driving window
        if duty > 14:
            raise serializers.ValidationError(
                {
                    "on_duty_hours": (
                        "On-duty hours cannot exceed "
                        "14 hours per duty period."
                    )
                }
            )

        # FMCSA 60-hour / 7-day cycle limit
        if cycle == "60" and used > 60:
            raise serializers.ValidationError(
                {
                    "cycle_hours_used": (
                        "Cannot exceed 60 hours "
                        "in a 7-day cycle."
                    )
                }
            )

        # FMCSA 70-hour / 8-day cycle limit
        if cycle == "70" and used > 70:
            raise serializers.ValidationError(
                {
                    "cycle_hours_used": (
                        "Cannot exceed 70 hours "
                        "in an 8-day cycle."
                    )
                }
            )

        return attrs