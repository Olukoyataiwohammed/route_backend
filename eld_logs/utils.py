from datetime import datetime, timedelta

from django.utils import timezone



def current_timestamp() -> datetime:
    """
    Return current timezone-aware timestamp.
    """
    return timezone.now()



def hours_to_timedelta(
    hours: float
) -> timedelta:
    """
    Convert decimal hours to timedelta.

    Example:
        8.5 -> 8 hours 30 minutes
    """
    return timedelta(
        hours=hours
    )



def timedelta_to_hours(
    duration: timedelta
) -> float:
    """
    Convert timedelta back to decimal hours.

    Example:
        timedelta(hours=8.5)
        -> 8.5
    """

    return round(
        duration.total_seconds() / 3600,
        2
    )



def format_hours(
    hours: float
) -> str:
    """
    Convert decimal hours into HH:MM format.

    Example:
        8.5 -> "08:30"
    """

    total_minutes = int(
        hours * 60
    )

    hrs = total_minutes // 60

    mins = total_minutes % 60

    return f"{hrs:02}:{mins:02}"



def calculate_remaining(
    limit: float,
    used: float
) -> float:
    """
    Calculate remaining available hours.

    Never returns negative values.
    """

    return max(
        round(limit - used, 2),
        0
    )



def is_limit_exceeded(
    limit: float,
    used: float
) -> bool:
    """
    Check if an FMCSA limit has been exceeded.
    """

    return used > limit



def calculate_cycle_total(
    hours_list: list[float]
) -> float:
    """
    Calculate total cycle hours.

    Example:
        [8, 10, 9]
        returns 27
    """

    if not hours_list:
        return 0.0

    return round(
        sum(hours_list),
        2
    )



def can_take_restart(
    off_duty_hours: float
) -> bool:
    """
    Check FMCSA 34-hour restart eligibility.
    """

    return off_duty_hours >= 34



def requires_break(
    driving_hours: float
) -> bool:
    """
    FMCSA rule:

    A driver requires a 30-minute break
    after 8 cumulative driving hours.
    """

    return driving_hours >= 8



def calculate_end_time(
    start_time: datetime,
    duration_hours: float
) -> datetime:
    """
    Calculate trip end time.

    Example:
        Start 08:00
        Duration 5 hours

        Returns 13:00
    """

    return start_time + timedelta(
        hours=duration_hours
    )