from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trips.models import Trip

from .models import ELDLog
from .services import ELDLogService


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_eld_log(request, pk):
    """
    Generate an ELD log from an existing trip.
    """

    trip = get_object_or_404(
        Trip,
        pk=pk,
        driver=request.user,
    )

    service = ELDLogService()

    cycle_hours_used = float(
        trip.current_cycle_used
    )

    # Estimated values
    driving_hours = min(11, cycle_hours_used)

    on_duty_hours = min(
        14,
        driving_hours + 1,
    )

    cycle_type = "70"

    adverse_conditions = False

    summary = service.generate_daily_summary(
        driving_hours=driving_hours,
        on_duty_hours=on_duty_hours,
        cycle_hours_used=cycle_hours_used,
        cycle_type=cycle_type,
        adverse_conditions=adverse_conditions,
    )

    eld_log = ELDLog.objects.create(
        driver=request.user,
        driving_hours=driving_hours,
        on_duty_hours=on_duty_hours,
        cycle_hours_used=cycle_hours_used,
        cycle_type=cycle_type,
        adverse_conditions=adverse_conditions,
        remaining_driving_hours=summary[
            "remaining_driving_hours"
        ],
        remaining_on_duty_hours=summary[
            "remaining_on_duty_hours"
        ],
        remaining_cycle_hours=summary[
            "remaining_cycle_hours"
        ],
        break_required=summary[
            "break_required"
        ],
        off_duty_reset_required=summary[
            "off_duty_reset_required"
        ],
        hos_violations=summary[
            "hos_violations"
        ],
    )

    return Response(
        {
            "message": "ELD log generated successfully.",
            "trip_id": str(trip.id),
            "summary": summary,
            "eld_log": {
                "id": eld_log.id,
                "driving_hours": eld_log.driving_hours,
                "on_duty_hours": eld_log.on_duty_hours,
                "cycle_hours_used": eld_log.cycle_hours_used,
                "remaining_driving_hours": eld_log.remaining_driving_hours,
                "remaining_on_duty_hours": eld_log.remaining_on_duty_hours,
                "remaining_cycle_hours": eld_log.remaining_cycle_hours,
                "break_required": eld_log.break_required,
                "off_duty_reset_required": eld_log.off_duty_reset_required,
                "hos_violations": eld_log.hos_violations,
            },
        },
        status=status.HTTP_201_CREATED,
    )