from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "driver",
        "pickup_location",
        "dropoff_location",
        "current_cycle_used",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "driver__username",
        "current_location",
        "pickup_location",
        "dropoff_location",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Trip Information",
            {
                "fields": (
                    "current_location",
                    "pickup_location",
                    "dropoff_location",
                    "current_cycle_used",
                    "status",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.driver = request.user
        super().save_model(request, obj, form, change)