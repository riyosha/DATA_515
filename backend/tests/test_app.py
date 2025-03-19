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

    @patch("src.helpers.scrapers.movie_details_scraper")
    @patch("src.helpers.scrapers.scrape_reviews")
    @patch("src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.get_results")
    @patch("src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.read_reviews")
    def test_scraping_movie_details_success(
        self, mock_read_reviews, mock_get_results,
        mock_scrape_reviews, mock_movie_details_scraper
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

    @patch("src.helpers.scrapers.movie_details_scraper")
    def test_scraping_movie_details_invalid_url(self, mock_movie_details_scraper):
        """Test movie details scraping with an invalid URL."""
        mock_movie_details_scraper.side_effect = ValueError("Invalid URL")
        response = self.client.post("/movie_details", json={"film_url": "invalid_url"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    @patch("src.helpers.scrapers.movie_details_scraper")
    @patch("src.helpers.scrapers.scrape_reviews")
    @patch("src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.get_results")
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

    @patch("src.helpers.scrapers_roast.scrape_user_reviews")
    @patch("src.helpers.scrapers_roast.scrape_user_stats")
    @patch("src.helpers.roast_generator.LetterboxdRoastAnalyzer.get_results")
    def test_username_roast_success(
        self, mock_get_results, mock_scrape_user_stats, mock_scrape_user_reviews
    ):
        """Test successful username roasting based on Letterboxd profile."""
        mock_scrape_user_reviews.return_value = ["Review 1", "Review 2"]
        mock_scrape_user_stats.return_value = {
            "total_reviews": 50,
            "favorite_directors": ["Nolan", "Tarantino"],
            "average_rating": 3.5,
        }
        mock_get_results.return_value = "Your taste in movies is questionable, but entertaining."

        response = self.client.post("/roast", json={"username": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("roast", data)

    def test_username_roast_missing_username(self):
        """Test username roast with missing username field."""
        response = self.client.post("/roast", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    @patch("src.helpers.scrapers.scrape_reviews")
    @patch("src.helpers.scrapers_roast.scrape_user_reviews")
    @patch("src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.get_taste_match_result")
    def test_taste_match_success(
        self, mock_get_taste_match_result, mock_scrape_user_reviews, mock_scrape_reviews
    ):
        """Test successful taste match analysis."""
        mock_scrape_reviews.return_value = ["Review 1", "Review 2"]
        mock_scrape_user_reviews.return_value = ["User Review 1", "User Review 2"]
        mock_get_taste_match_result.return_value = "You might like this movie!"

        response = self.client.post(
            "/taste", json={"film_url": "https://letterboxd.com/film/mickey-17/", 
            "username": "test_user"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("taste", data)

    def test_taste_match_missing_username(self):
        """Test taste match with missing username field."""
        response = self.client.post(
            "/taste", json={"film_url": "https://letterboxd.com/film/mickey-17/"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_taste_match_missing_film_url(self):
        """Test taste match with missing film URL."""
        response = self.client.post("/taste", json={"username": "test_user"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    @patch("src.helpers.scrapers.scrape_reviews")
    @patch("src.helpers.scrapers_roast.scrape_user_reviews")
    @patch("src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.get_taste_match_result")
    def test_taste_match_key_error(
        self, _mock_get_taste_match_result, _mock_scrape_user_reviews, _mock_scrape_reviews
    ):
        """Test taste match with a missing key in the JSON."""
        response = self.client.post("/taste",json={
            "film_url":"https://letterboxd.com/film/mickey-17/"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
