"""
Unit tests for the Flask application.
"""

import unittest
from unittest.mock import patch
import requests
from src.app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask application."""

    def setUp(self):
        """Set up the test client."""
        app.testing = True
        self.client = app.test_client()

    @patch("helpers.scrapers.movie_details_scraper")
    @patch("helpers.scrapers.scrape_reviews")
    @patch("helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.get_results")
    @patch("helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.read_reviews")
    def test_scraping_movie_details_success(
        self, mock_read_reviews, mock_get_results, mock_scrape_reviews, mock_movie_details_scraper
    ):
        """Test successful movie details scraping with summary and aspects."""
        mock_movie_details_scraper.return_value = {
            "movie_name": "Mickey 17",
            "director": "Bong Joon Ho",
            "year": "2025",
            "genres": "Comedy, Adventure, Science Fiction",
            "synopsis": (
                "Unlikely hero Mickey Barnes finds himself in the extraordinary circumstance of "
                "working for an employer who demands the ultimate commitment to the job… to die, "
                "for a living."
            ),
            "backdrop_image_url": (
                "https://a.ltrbxd.com/resized/sm/upload/ce/wj/ed/wq/"
                "7Oh1xRB8QbMduhqXEUHKlnwxMJi-1200-1200-675-675-crop-000000.jpg?v=c4a2895be9"
            ),
        }
        mock_scrape_reviews.return_value = ["Review 1", "Review 2"]
        mock_read_reviews.return_value = "Processed review text"
        mock_get_results.return_value = (
            "Summary of reviews",
            [
                ["Robert Pattinson", 74, 2],
                ["Bong Joon-Ho", 52, 11],
                ["Humor/Comedy", 40, 13],
                ["Satire", 24, 19],
                ["Visuals", 18, 1],
            ],
        )

        response = self.client.post(
            "/movie_details", json={"film_url": "https://letterboxd.com/film/mickey-17/"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("movie_details", data)
        self.assertIn("summary", data)
        self.assertIn("aspects", data)

    def test_scraping_movie_details_missing_url(self):
        """Test movie details scraping with a missing URL."""
        response = self.client.post("/movie_details", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    @patch("helpers.scrapers.movie_details_scraper")
    def test_scraping_movie_details_invalid_url(self, mock_movie_details_scraper):
        """Test movie details scraping with an invalid URL."""
        mock_movie_details_scraper.side_effect = ValueError("Invalid URL")
        response = self.client.post("/movie_details", json={"film_url": "invalid_url"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    @patch("helpers.scrapers.movie_details_scraper")
    @patch("helpers.scrapers.scrape_reviews")
    @patch("helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.get_results")
    def test_scraping_movie_details_request_exception(
        self, _mock_get_results, _mock_scrape_reviews, mock_movie_details_scraper
    ):
        """Test movie details scraping when an external request fails."""
        mock_movie_details_scraper.side_effect = requests.exceptions.RequestException("Failed")
        response = self.client.post(
            "/movie_details", json={"film_url": "https://letterboxd.com/film/mickey-17/"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
