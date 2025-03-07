"""Test suite for the Letterboxd scrapers.py helping functions"""

import unittest
import csv
import os
from unittest.mock import patch

from backend.src.helpers.scrapers import validate_letterboxd_film_url, fetch_reviews, ScraperError
from backend.src.helpers.scrapers import scrape_reviews, movie_details_scraper

# Test suite for testing the Letterboxd scraper functionality
class TestLetterboxdScraper(unittest.TestCase):
    """Unit tests for the Letterboxd scraper functions."""

    def test_valid_url(self):
        """Test valid URL."""
        self.assertEqual(
            validate_letterboxd_film_url("https://letterboxd.com/film/the-brutalist/"), True
        )

    def test_invalid_url(self):
        """Test invalid URL."""
        self.assertEqual(
            validate_letterboxd_film_url(
                "https://letterboxd.com/thediegoandaluz/film/the-brutalist/"
            ),
            False,
        )

    def test_valid_movie_details_scraper(self):
        """Test movie details scraper for valid URL."""
        movie_details_scraper("https://letterboxd.com/film/moonfall/")
        self.assertTrue(os.path.exists("moonfall_details.csv"))
        self.assertTrue(os.path.exists("moonfall_image.jpg"))
        with open(
            "moonfall_details.csv", mode="r", newline="", encoding="utf-8"
        ) as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            expected_columns = ["Year", "Director", "Genres", "Synopsis"]
            self.assertTrue(
                all(col in header for col in expected_columns),
                "CSV columns are incorrect.",
            )
            first_row = next(csv_reader)
            self.assertFalse(
                any(field == "" for field in first_row),
                "First row contains empty values.",
            )
        os.remove("moonfall_details.csv")
        os.remove("moonfall_image.jpg")

    def test_valid_scrape_reviews(self):
        """Test review scraping for valid movie."""
        scrape_reviews("https://letterboxd.com/film/moonfall/", n=2)
        self.assertTrue(os.path.exists("moonfall_reviews.csv"))
        with open("moonfall_reviews.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertGreater(len(rows), 1)  # At least header + 1 row
        os.remove("moonfall_reviews.csv")

    @patch("requests.get")
    def test_failed_http_request_fetch_reviews(self, mock_get):
        """Test fetch reviews when HTTP request fails."""
        valid_url = "https://letterboxd.com/film/moonfall/"
        mock_get.return_value.status_code = 404  # Simulating failed HTTP request
        headers = {"User-Agent": "Mozilla/5.0"}
        with self.assertRaises(ScraperError) as context:
            fetch_reviews(valid_url, headers)
        self.assertIn("Failed to get reviews", str(context.exception))


# Running the tests
if __name__ == "__main__":
    unittest.main()
