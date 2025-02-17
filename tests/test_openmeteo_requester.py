import sys, os
sys.path.append(os.path.abspath("../")) # Adding cyclonic-data root directory to path so that all modules are discoverable

from unittest import TestCase
import unittest

from cyclonic_requests.request_enums import OpenMeteoRequestParam
from cyclonic_requests.openmeteo_requester import OpenMeteoRequester

class TestOpenMeteoRequester(TestCase):
    def setUp(self):
        self.requester = OpenMeteoRequester()

    def test_prepare_request_with_default_values(self):
        options = [OpenMeteoRequestParam.TEMP_2M]
        result = self.requester.prepare_request(options)

        expected_result = { 
            "latitude": 51.8413,
            "longitude": -8.4911,
            "hourly": ["temperature_2m"]
        }

        self.assertEqual(result, expected_result)

    def test_prepare_request_with_custom_coords(self):
        options = [OpenMeteoRequestParam.TEMP_2M]
        result = self.requester.prepare_request(lat=52.52, long=-7.12, options=options)

        expected_result = { 
            "latitude": 52.52,
            "longitude": -7.12,
            "hourly": ["temperature_2m"]
        }

        self.assertEqual(result, expected_result)

    def test_prepare_request_with_all_custom_values(self):
        options = [OpenMeteoRequestParam.TEMP_2M, OpenMeteoRequestParam.WD_10M, OpenMeteoRequestParam.WS_10M]
        result = self.requester.prepare_request(lat=52.52, long=-7.12, options=options)

        expected_result = {
            "latitude": 52.52, 
            "longitude": -7.12,
            "hourly": ["temperature_2m", "wind_direction_10m", "wind_speed_10m"]
        }

        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()