import sys, os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath("../")) # Adding cyclonic-data root directory to path so that all modules are discoverable

from unittest import TestCase
from unittest.mock import patch

from pathlib import Path
from pandas import DataFrame

from cyclonic_formatting.openmeteo_formatter import OpenMeteoFormatter
from cyclonic_requests.openmeteo_requester import OpenMeteoRequester

import json

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
        
    def test_empty_dataframe_input(self):
        empty_df = DataFrame()
        result_path = self.formatter.write(empty_df, previous=True)

        with open(result_path, "r", encoding="utf-8") as f:
            content = f.read()
            parsed = json.loads(content)  # Handles spacing and formatting
            self.assertEqual(parsed, [])  # Confirm it's a valid empty JSON array

        result_path.unlink()

    def test_none_input_raises_error(self):
        with self.assertRaises(AttributeError):  # or TypeError if you do type-checking in write()
            self.formatter.write(None, previous=False)

    def test_list_input_raises_error(self):
        with self.assertRaises(AttributeError):  # or a custom validation error if implemented
            self.formatter.write(["invalid", "data"], previous=True)

    def test_string_input_raises_error(self):
        with self.assertRaises(AttributeError):
            self.formatter.write("this is not a DataFrame", previous=False)

    
    def test_to_json_failure_handled(self):
        df = DataFrame({"a": ["test"]})
        with patch.object(df, "to_json", side_effect=IOError("Disk error")):
            with self.assertRaises(IOError):  # or your custom error type
                self.formatter.write(df, previous=True)

    def test_invalid_output_path(self):
        # Temporarily redirect OUTPUT_PATH to a bad location
        bad_formatter = OpenMeteoFormatter()
        bad_formatter.OUTPUT_PATH = Path("/invalid/::path")  # Invalid on most OSs

        with self.assertRaises((OSError, IOError)):
            bad_formatter.write(DataFrame({"a": ["test"]}), previous=True)