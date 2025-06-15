from cyclonic_requests.openmeteo_requester import OpenMeteoRequester
from cyclonic_requests.request_enums import OpenMeteoRequestParam
from cyclonic_formatting.openmeteo_formatter import OpenMeteoFormatter
from utils.geo import haversine

from utils.logger import logger_setup
logger = logger_setup(name="REQCTRL")

from pathlib import Path

import json

class RequestController:
    def __init__(self):
        self.om_requester = OpenMeteoRequester()
        self.om_formatter = OpenMeteoFormatter()

    def send_om_request(self, options: list[OpenMeteoRequestParam], previous: bool = False, days : int = 30, lat: float = 51.8413, long: float = -8.4911):
        logger.debug("Preparing request parameters...")
        try:
            params = self.om_requester.prepare_request(options, num_days=days, previous=previous, lat=lat, long=long)

            logger.debug("Sending OpenMeteo request...")
            response = self.om_requester.send_request(params, previous=previous)

            return response
        except Exception as e:
            logger.error(e)
            exit(1)

    def get_weather_data(self, options: list[OpenMeteoRequestParam], previous: bool = False, days: int = 30, lat: float = 51.8413, long: float = -8.4911):
        logger.debug("Sending request for first location...")

        locations = self.get_locations_to_fetch(lat, long)
        
        first_response = self.send_om_request(
            options=options,
            days=days,
            previous=previous,
            lat=locations["primary"][0],
            long=locations["primary"][1]
        )

        first_result = self.om_formatter.format_data(first_response)

        second_response = self.send_om_request(
            options=options,
            days=days,
            previous=previous,
            lat=locations["secondary"][0],
            long=locations["secondary"][1]
        )

        second_result = self.om_formatter.format_data(second_response)

        return first_result, second_result

    def get_locations_to_fetch(self, primary_lat: float, primary_long: float) -> dict:
        """
        Returns the co-ordinates of the most meaningful station which would yield the best results during training based on the primary locatoin picked.
        """

        secondary_candidates = self.find_second_location(primary_lat, primary_long)
        secondary = secondary_candidates[0] if secondary_candidates else None

        return {
            "primary": (primary_lat, primary_long),
            "secondary": (secondary[1]["lat"], secondary[1]["long"]) if secondary else None
        }

    def find_second_location(self, lat: float, long: float, min_km: int = 50, max_km: int = 500) -> list[dict]:
        """
        Finds the most suitable location with similar conditions.
        """
        results = []

        JSON_PATH = Path(Path("").cwd(), "./common_stations.json")

        with JSON_PATH.open("r") as f:
            candidates: list[dict] = json.load(f)

        for c in candidates:
            d = haversine(lat, long, c["lat"], c["long"])
            if min_km <= d <= max_km:
                results.append((d, c))

        return sorted(results, key=lambda x: x[0])