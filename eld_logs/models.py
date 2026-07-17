from django.db import models
from django.conf import settings


class ELDLog(models.Model):
    """
    Electronic Logging Device (ELD) log.

    Stores driver's FMCSA Hours of Service information.
    """

    CYCLE_CHOICES = [
        ("60", "60-hour / 7-day"),
        ("70", "70-hour / 8-day"),
    ]

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eld_logs",
    )

    driving_hours = models.FloatField()

    on_duty_hours = models.FloatField()

    cycle_hours_used = models.FloatField()

    cycle_type = models.CharField(
        max_length=2,
        choices=CYCLE_CHOICES,
        default="70",
    )

    adverse_conditions = models.BooleanField(
        default=False
    )

    remaining_driving_hours = models.FloatField(
        default=0
    )

    remaining_on_duty_hours = models.FloatField(
        default=0
    )

    remaining_cycle_hours = models.FloatField(
        default=0
    )

    break_required = models.BooleanField(
        default=False
    )

    off_duty_reset_required = models.BooleanField(
        default=False
    )

    hos_violations = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return (
            f"{self.driver} - "
            f"{self.created_at.strftime('%Y-%m-%d')}"
        )