"""Unit tests for the Flask application."""

import unittest
from unittest.mock import patch
from src.app import app

class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask application."""
    
    def setUp(self):
        """Set up the test client."""
        app.testing = True
        self.client = app.test_client()

    @patch("helpers.scrapers.movie_details_scraper")
    def test_scraping_movie_details_success(self, mock_movie_details_scraper):
        """Test successful movie details scraping."""
        mock_movie_details_scraper.return_value = {"title": "Example Movie", "year": "2024"}
        response = self.client.post(
            "/movie_details", json={"film_url": "https://letterboxd.com/film/mickey-17/"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("movie_details", data)

    @patch("helpers.scrapers.movie_details_scraper")
    def test_scraping_movie_details_missing_url(self, mock_movie_details_scraper):
        """Test movie details scraping with a missing URL."""
        del mock_movie_details_scraper 
        response = self.client.post("/movie_details", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    @patch("helpers.scrapers.scrape_reviews")
    @patch("helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.get_results")
    def test_summary_aspects_success(self, mock_get_results, mock_scrape_reviews):
        """Test successful summary and aspect analysis."""
        mock_scrape_reviews.return_value = ["Review 1", "Review 2"]
        mock_get_results.return_value = ("Summary of reviews", {"aspect1": "positive"})
        response = self.client.post(
            "/summary_aspects", json={"film_url": "https://letterboxd.com/film/mickey-17/"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("summary", data)
        self.assertIn("aspects", data)

    @patch("helpers.scrapers.scrape_reviews")
    def test_summary_aspects_missing_url(self, mock_scrape_reviews):
        """Test summary and aspect analysis with a missing URL."""
        del mock_scrape_reviews  # Unused mock
        response = self.client.post("/summary_aspects", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    @patch("helpers.scrapers.scrape_reviews")
    def test_summary_aspects_invalid_url(self, mock_scrape_reviews):
        """Test summary and aspect analysis with an invalid URL."""
        mock_scrape_reviews.side_effect = Exception("Invalid URL")
        response = self.client.post("/summary_aspects", json={"film_url": "invalid_url"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
