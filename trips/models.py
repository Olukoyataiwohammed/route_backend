from django.conf import settings
from django.db import models
import uuid


class Trip(models.Model):

    class TripStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PLANNED = "PLANNED", "Planned"
        COMPLETED = "COMPLETED", "Completed"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trips",
    )

    current_location = models.CharField(
        max_length=255,
        help_text="Driver's current location",
    )

    pickup_location = models.CharField(
        max_length=255,
        help_text="Pickup location",
    )

    dropoff_location = models.CharField(
        max_length=255,
        help_text="Dropoff location",
    )

    current_cycle_used = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Current HOS cycle hours used",
    )

    status = models.CharField(
        max_length=20,
        choices=TripStatus.choices,
        default=TripStatus.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "trips"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.driver.username} - "
            f"{self.pickup_location} → {self.dropoff_location}"
        )