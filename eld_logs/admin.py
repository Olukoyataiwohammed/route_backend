from django.contrib import admin



from .models import ELDLog


@admin.register(ELDLog)
class ELDLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for ELD logs.
    """

    list_display = (
        "driver",
        "driving_hours",
        "on_duty_hours",
        "cycle_hours_used",
        "cycle_type",
        "adverse_conditions",
        "break_required",
        "off_duty_reset_required",
        "created_at",
    )

    list_filter = (
        "cycle_type",
        "adverse_conditions",
        "break_required",
        "off_duty_reset_required",
        "created_at",
    )

    search_fields = (
        "driver__username",
        "driver__email",
    )

    readonly_fields = (
        "remaining_driving_hours",
        "remaining_on_duty_hours",
        "remaining_cycle_hours",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Driver Information",
            {
                "fields": (
                    "driver",
                ),
            },
        ),
        (
            "Hours of Service",
            {
                "fields": (
                    "driving_hours",
                    "on_duty_hours",
                    "cycle_hours_used",
                    "cycle_type",
                ),
            },
        ),
        (
            "FMCSA Compliance",
            {
                "fields": (
                    "adverse_conditions",
                    "break_required",
                    "off_duty_reset_required",
                ),
            },
        ),
        (
            "Calculated Values",
            {
                "fields": (
                    "remaining_driving_hours",
                    "remaining_on_duty_hours",
                    "remaining_cycle_hours",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )