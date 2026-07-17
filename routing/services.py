from typing import Any
import requests

from django.conf import settings


class RouteService:
    """
    Service responsible for route planning.
    """

    FUEL_STOP_INTERVAL_MILES = 1000
    AVERAGE_TRUCK_SPEED_MPH = 55

    ORS_API_KEY = settings.ORS_API_KEY

    GEOCODE_URL = (
        "https://api.openrouteservice.org/geocode/search"
    )

    DIRECTIONS_URL = (
    "https://api.openrouteservice.org/v2/directions/driving-hgv/geojson"
)

    # ----------------------------
    # Existing methods
    # ----------------------------

    def calculate_route(
    self,
    current_location: str,
    pickup_location: str,
    dropoff_location: str,
    ) -> dict[str, Any]:

        current = self.geocode_location(current_location)
        pickup = self.geocode_location(pickup_location)
        dropoff = self.geocode_location(dropoff_location)

        headers = {
            "Authorization": self.ORS_API_KEY,
            "Content-Type": "application/json",
        }

        body = {
            "coordinates": [
                current,
                pickup,
                dropoff,
            ]
        }

        try:
            response = requests.post(
                self.DIRECTIONS_URL,
                json=body,
                headers=headers,
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as e:
            raise Exception(
                f"Route generation failed: {str(e)}"
            )

        print("ORS Response:")
        print(data)

        if "features" not in data:
            raise Exception(f"OpenRouteService Error: {data}")

        feature = data["features"][0]

        summary = feature["properties"]["summary"]

        coordinates = feature["geometry"]["coordinates"]

        distance_meters = summary["distance"]
        duration_seconds = summary["duration"]

        distance_miles = round(
            distance_meters * 0.000621371,
            2,
        )

        driving_hours = round(
            duration_seconds / 3600,
            2,
        )
        

        return {
        "current_location": current_location,
        "pickup_location": pickup_location,
        "dropoff_location": dropoff_location,

        "current_coordinates": current,
        "pickup_coordinates": pickup,
        "dropoff_coordinates": dropoff,

        "distance_miles": distance_miles,
        "driving_time_hours": driving_hours,
        "coordinates": [
            [point[1], point[0]]
            for point in coordinates
        ],

        "fuel_stops": self.calculate_fuel_stops(distance_miles),

        "directions": feature["properties"].get(
            "segments",
            [],
        ),

        }

    def estimate_driving_time(
        self,
        distance_miles: float,
    ) -> float:

        if distance_miles <= 0:
            return 0.0

        return round(
            distance_miles / self.AVERAGE_TRUCK_SPEED_MPH,
            2,
        )

    def calculate_fuel_stops(
        self,
        distance_miles: float,
    ) -> list[dict[str, Any]]:

        fuel_stops = []

        if distance_miles <= self.FUEL_STOP_INTERVAL_MILES:
            return fuel_stops

        stop_number = 1
        current_mile = self.FUEL_STOP_INTERVAL_MILES

        while current_mile < distance_miles:
            fuel_stops.append(
                {
                    "stop_number": stop_number,
                    "mile_marker": current_mile,
                    "reason": "Fuel Stop",
                }
            )

            stop_number += 1
            current_mile += self.FUEL_STOP_INTERVAL_MILES

        return fuel_stops

    def calculate_remaining_distance(
        self,
        total_distance: float,
        distance_completed: float,
    ) -> float:

        remaining = total_distance - distance_completed

        return max(round(remaining, 2), 0)

    def calculate_remaining_driving_time(
        self,
        remaining_distance: float,
    ) -> float:

        return self.estimate_driving_time(
            remaining_distance
        )

    # ----------------------------
    # NEW METHOD
    # ----------------------------

    def geocode_location(
        self,
        location: str,
    ) -> list[float]:

        headers = {
            "Authorization": self.ORS_API_KEY,
        }

        params = {
            "text": location,
            "size": 1,
        }

        response = requests.get(
            self.GEOCODE_URL,
            headers=headers,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

        features = data.get("features", [])

        if not features:
            raise Exception(
                f"Location not found: {location}"
            )

        lon, lat = features[0]["geometry"]["coordinates"]

        return [lon, lat]