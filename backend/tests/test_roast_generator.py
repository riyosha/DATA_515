"""
Unit tests for the LetterboxdRoastAnalyzer module.
"""

import unittest
from unittest.mock import patch, MagicMock

from src.helpers.roast_generator import (
    LetterboxdRoastAnalyzer,
    RoastGenerationError,
)


class TestLetterboxdRoastAnalyzer(unittest.TestCase):
    """Unit tests for the LetterboxdRoastAnalyzer class."""

    def setUp(self):
        """Create an instance of LetterboxdRoastAnalyzer for testing."""
        self.analyzer = LetterboxdRoastAnalyzer()

    # Tests for read_user_data
    def test_read_user_data_valid(self):
        """Test that read_user_data returns correctly formatted text."""
        reviews = [
            {"review_text": "Great movie!"},
            {"review_text": "I loved the cinematography."},
        ]
        stats = {"total_hours_watched": 120, "num_years": 5}
        result = self.analyzer.read_user_data(reviews, stats)
        self.assertIn("User Reviews:", result)
        self.assertIn("Great movie!", result)
        self.assertIn("I loved the cinematography.", result)
        self.assertIn("Total Hours Watched: 120", result)
        self.assertIn("Num Years: 5", result)

    def test_read_user_data_empty_reviews(self):
        """Test that read_user_data raises ValueError if reviews_list is empty."""
        reviews = []
        stats = {"total_hours_watched": 120}
        with self.assertRaises(ValueError):
            self.analyzer.read_user_data(reviews, stats)

    def test_read_user_data_empty_stats(self):
        """Test that read_user_data uses default stats message if stats_dict is empty."""
        reviews = [{"review_text": "Amazing experience."}]
        stats = {}
        result = self.analyzer.read_user_data(reviews, stats)
        self.assertIn("No statistics available.", result)

    # Tests for generate_roast
    @patch("src.helpers.roast_generator.genai.GenerativeModel")
    @patch("src.helpers.roast_generator.genai.configure")
    def test_generate_roast_success(self, _mock_configure, mock_model_class):
        """Test generate_roast returns a roast when the API responds correctly."""
        fake_response = MagicMock()
        fake_response.text = "Savage roast text."
        fake_model = MagicMock()
        fake_model.generate_content.return_value = fake_response
        mock_model_class.return_value = fake_model

        user_data = (
            "User Reviews: Great movie!\n\n"
            "User Statistics: Total Hours Watched: 120"
        )
        roast = self.analyzer.generate_roast(user_data, "fake-api-key")
        self.assertEqual(roast, "Savage roast text.")
        args, _ = fake_model.generate_content.call_args
        prompt = args[0]
        self.assertIn("guilty_pleasure_movie", prompt)
        self.assertIn("unpopular_opinion", prompt)

    @patch("src.helpers.roast_generator.genai.GenerativeModel")
    @patch("src.helpers.roast_generator.genai.configure")
    def test_generate_roast_too_long(self, _mock_configure, mock_model_class):
        """Test generate_roast raises RoastGenerationError if the roast is too long."""
        fake_response = MagicMock()
        fake_response.text = "word " * 711  # 711 words.
        fake_model = MagicMock()
        fake_model.generate_content.return_value = fake_response
        mock_model_class.return_value = fake_model

        user_data = "User Reviews: Test\n\nUser Statistics: Test"
        with self.assertRaises(RoastGenerationError):
            self.analyzer.generate_roast(user_data, "fake-api-key")

    # Tests for get_results
    @patch.object(LetterboxdRoastAnalyzer, "generate_roast")
    def test_get_results_success(self, mock_generate_roast):
        """
        Test get_results returns a roast when generate_roast succeeds
        using the first valid API key.
        """
        fake_roast = "Savage roast generated."
        mock_generate_roast.return_value = fake_roast

        reviews = [{"review_text": "Great movie!"}]
        stats = {"num_years": 5}
        api_keys = ["key1", "key2"]
        result = self.analyzer.get_results(reviews, stats, api_keys)
        self.assertEqual(result, fake_roast)
        mock_generate_roast.assert_called_once()

    @patch.object(LetterboxdRoastAnalyzer, "generate_roast")
    def test_get_results_failure(self, mock_generate_roast):
        """
        Test get_results raises RoastGenerationError if generate_roast fails
        for all provided API keys.
        """
        mock_generate_roast.side_effect = Exception("API error")
        reviews = [{"review_text": "Average movie."}]
        stats = {"total_hours_watched": 100}
        api_keys = ["key1", "key2", "key3"]
        with self.assertRaises(RoastGenerationError):
            self.analyzer.get_results(reviews, stats, api_keys)


if __name__ == "__main__":
    unittest.main()
