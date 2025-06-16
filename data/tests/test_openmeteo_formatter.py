import sys, os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath("../")) # Adding cyclonic-data root directory to path so that all modules are discoverable

from unittest import TestCase
import unittest

from pathlib import Path
from pandas import DataFrame

from cyclonic_formatting.openmeteo_formatter import OpenMeteoFormatter
from cyclonic_requests.openmeteo_requester import OpenMeteoRequester

class TestOpenMeteoFormatter(TestCase):
    def setUp(self):
        self.formatter = OpenMeteoFormatter()
        self.test_df = DataFrame({"a": ["test"]})

    def test_past_file_name_correct(self):
        result_path = self.formatter.write(self.test_df, previous=True)

        # Check filename pattern
        self.assertIn("result_past_", result_path.name)
        self.assertTrue(result_path.name.endswith(".json"))

        # Check Directory path
        self.assertIn("past", result_path.parts)
        
        # Ensure file was created
        self.assertTrue(result_path.exists())
        self.assertTrue(result_path.is_file())

        result_path.unlink()

    def test_forecast_file_name_correct(self):
        result_path = self.formatter.write(self.test_df, previous=False)

        # Check filename pattern
        self.assertIn("result_forecast_", result_path.name)
        self.assertTrue(result_path.name.endswith(".json"))

        # Check Directory path
        self.assertIn("forecast", result_path.parts)

        # Ensure file was created
        self.assertTrue(result_path.exists())
        self.assertTrue(result_path.is_file())

        result_path.unlink()
        
    