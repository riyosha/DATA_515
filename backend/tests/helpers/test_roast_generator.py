"""
Test suite for the roast_generator.py helper functions.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from src.helpers.roast_generator import generate_funny_roast, main


class TestRoastGenerator(unittest.TestCase):
    """Unit tests for the Letterboxd Roast Generator functions."""

    @patch("src.helpers.roast_generator.genai.GenerativeModel")
    @patch("src.helpers.roast_generator.pd.read_csv")
    @patch("src.helpers.roast_generator.os.path.exists")
    @patch("builtins.print")
    def test_generate_funny_roast_success(self, mock_print, mock_exists,
                                          mock_read_csv, mock_generative_model):
        """
        Test successful roast generation when both reviews and stats files exist.
        """
        # Simulate that the stats file exists.
        mock_exists.return_value = True

        # Create dummy DataFrames for reviews and stats.
        dummy_reviews_df = pd.DataFrame({"Review": ["Great movie!"]})
        dummy_stats_df = pd.DataFrame({"Stat": ["100 hours watched"]})

        # When pd.read_csv is called, first return reviews, then stats.
        mock_read_csv.side_effect = [dummy_reviews_df, dummy_stats_df]

        # Setup a dummy Gemini response.
        dummy_response = MagicMock()
        dummy_response.text = "This is a savage roast."
        dummy_model = MagicMock()
        dummy_model.generate_content.return_value = dummy_response
        mock_generative_model.return_value = dummy_model

        # Call the function.
        generate_funny_roast("dummyuser", "dummy_api_key")

        # Verify that generate_content was called.
        dummy_model.generate_content.assert_called()

        # Verify that the roast output was printed.
        mock_print.assert_any_call("\nYour Letterboxd Roast:\n")
        mock_print.assert_any_call("This is a savage roast.")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_api_key"})
    @patch("src.helpers.roast_generator.generate_funny_roast")
    @patch("builtins.input", return_value="dummyuser")
    def test_main_success(self, _, mock_generate):
        """
        Test that main() retrieves the API key and username, then calls generate_funny_roast.
        """
        main()
        mock_generate.assert_called_once_with("dummyuser", "dummy_api_key")

    @patch.dict(os.environ, {}, clear=True)
    def test_main_no_api_key(self):
        """
        Test that main() raises an EnvironmentError if the GEMINI_API_KEY is missing.
        """
        with self.assertRaises(EnvironmentError):
            main()


if __name__ == "__main__":
    unittest.main()
