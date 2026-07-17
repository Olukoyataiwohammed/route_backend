from math import radians, sin, cos, sqrt, atan2


def miles_to_kilometers(miles: float) -> float:
    """
    Convert miles to kilometers.
    """
    return round(miles * 1.60934, 2)


def kilometers_to_miles(kilometers: float) -> float:
    """
    Convert kilometers to miles.
    """
    return round(kilometers / 1.60934, 2)


def format_distance(distance: float) -> str:
    """
    Format distance for display.
    """
    return f"{distance:.2f} miles"


def format_duration(hours: float) -> str:
    """
    Convert decimal hours into hours and minutes.
    """

    whole_hours = int(hours)
    minutes = round((hours - whole_hours) * 60)

    if whole_hours == 0:
        return f"{minutes} min"

    if minutes == 0:
        return f"{whole_hours} hr"

    return f"{whole_hours} hr {minutes} min"


def validate_locations(
    current_location: str,
    pickup_location: str,
    dropoff_location: str,
) -> bool:
    """
    Ensure pickup and dropoff locations are different.
    """

    return pickup_location.strip().lower() != dropoff_location.strip().lower()


def calculate_straight_line_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate straight-line distance (Haversine formula).

    Returns:
        Distance in miles.
    """

    earth_radius = 3958.8

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(earth_radius * c, 2)