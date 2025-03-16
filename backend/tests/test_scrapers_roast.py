"""
Test suite for the scrapers_roast module functions.
"""

import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from src.helpers.scrapers_roast import (
    validate_letterboxd_user,
    fetch_html_content,
    parse_review_element,
    scrape_user_reviews,
    scrape_user_stats,
    ScraperError,
)


class FakeResponse:
    """A fake response object to simulate requests responses for testing.

    This class is used solely for testing purposes.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, text, status_code):
        """Initialize FakeResponse with the given text and status code."""
        self.text = text
        self.status_code = status_code


class TestScrapersRoast(unittest.TestCase):
    """Unit tests for the scrapers_roast module functions."""

    def test_validate_letterboxd_user_valid(self):
        """Test validate_letterboxd_user returns True for a valid user."""
        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            html = "<html><body><h1>Welcome</h1></body></html>"
            mock_get.return_value = FakeResponse(html, 200)
            self.assertTrue(validate_letterboxd_user("validuser"))

    def test_validate_letterboxd_user_invalid_status(self):
        """Test validate_letterboxd_user returns False when status is not 200."""
        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            mock_get.return_value = FakeResponse("Not Found", 404)
            self.assertFalse(validate_letterboxd_user("invaliduser"))

    def test_validate_letterboxd_user_invalid_content(self):
        """Test validate_letterboxd_user returns False for error page content."""
        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            html = (
                '<html><body class="error message-dark">'
                "<h1>Letterboxd</h1>"
                "<strong>Sorry, we can’t find the page you’ve requested.</strong>"
                "</body></html>"
            )
            mock_get.return_value = FakeResponse(html, 200)
            self.assertFalse(validate_letterboxd_user("invaliduser"))

    def test_fetch_html_content_success(self):
        """Test fetch_html_content returns HTML for a successful response."""
        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            html = "<html><body>Content</body></html>"
            mock_get.return_value = FakeResponse(html, 200)
            headers = {"User-Agent": "Mozilla/5.0"}
            result = fetch_html_content("http://example.com", headers)
            self.assertEqual(result, html)

    def test_fetch_html_content_failure(self):
        """Test fetch_html_content raises ScraperError for a non-200 response."""
        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            mock_get.return_value = FakeResponse("Error", 500)
            headers = {"User-Agent": "Mozilla/5.0"}
            with self.assertRaises(ScraperError):
                fetch_html_content("http://example.com", headers)

    def test_parse_review_element(self):
        """Test _parse_review_element extracts review details correctly."""
        html = (
            '<div class="film-detail-content">'
            '<h2 class="headline-2 prettify"><a href="/film/movie-slug/">'
            "Test Movie</a></h2>"
            '<small class="metadata"><a>2022</a></small>'
            '<span class="rating">4/5</span>'
            '<span class="date">Watched January 10, 2023</span>'
            '<div class="js-review-body">Amazing movie!</div>'
            "</div>"
        )
        soup = BeautifulSoup(html, "html.parser")
        element = soup.find("div", class_="film-detail-content")
        result = parse_review_element(element)
        expected = {
            "movie_name": "Test Movie",
            "movie_url": "https://letterboxd.com/film/movie-slug/",
            "movie_year": "2022",
            "rating": "4/5",
            "watched_date": "January 10, 2023",
            "review_text": "Amazing movie!",
        }
        self.assertEqual(result, expected)

    def test_scrape_user_reviews_valid(self):
        """Test scrape_user_reviews returns correct reviews for a valid user."""
        def side_effect(url, **_kwargs):
            if url == "https://letterboxd.com/testuser/":
                return FakeResponse("<html><body><h1>Welcome</h1></body></html>", 200)
            if "https://letterboxd.com/testuser/films/reviews/" in url:
                html = (
                    '<html><body>'
                    '<div class="film-detail-content">'
                    '<h2 class="headline-2 prettify"><a href="/film/test-movie/">'
                    "Test Movie</a></h2>"
                    '<small class="metadata"><a>2021</a></small>'
                    '<span class="rating">5/5</span>'
                    '<span class="date">Watched Feb 20, 2022</span>'
                    '<div class="js-review-body">Great review!</div>'
                    "</div>"
                    "</body></html>"
                )
                return FakeResponse(html, 200)
            return FakeResponse("", 404)

        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            mock_get.side_effect = side_effect
            reviews = scrape_user_reviews("testuser", n_pages=1)
            self.assertEqual(len(reviews), 1)
            expected = {
                "movie_name": "Test Movie",
                "movie_url": "https://letterboxd.com/film/test-movie/",
                "movie_year": "2021",
                "rating": "5/5",
                "watched_date": "Feb 20, 2022",
                "review_text": "Great review!",
            }
            self.assertEqual(reviews[0], expected)

    def test_scrape_user_reviews_invalid_user(self):
        """Test scrape_user_reviews raises ValueError for an invalid user."""
        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            mock_get.return_value = FakeResponse("Not Found", 404)
            with self.assertRaises(ValueError):
                scrape_user_reviews("nonexistentuser", n_pages=1)

    def test_scrape_user_stats_valid(self):
        """Test scrape_user_stats returns correct stats for a valid user."""
        def side_effect(url, **_kwargs):
            if url == "https://letterboxd.com/testuser/":
                return FakeResponse("<html><body><h1>Welcome</h1></body></html>", 200)
            if url == "https://letterboxd.com/testuser/stats":
                html = (
                    '<html><body>'
                    '<h4 class="yir-member-statistic statistic">3 years</h4>'
                    '<h4 class="yir-member-statistic statistic">150 hours</h4>'
                    '<h4 class="yir-member-statistic statistic">20 directors</h4>'
                    '<h4 class="yir-member-statistic statistic">8 countries</h4>'
                    '<h4 class="yir-member-statistic statistic">10 days</h4>'
                    '<h4 class="yir-member-statistic statistic">5 films</h4>'
                    "</body></html>"
                )
                return FakeResponse(html, 200)
            return FakeResponse("", 404)

        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            mock_get.side_effect = side_effect
            stats = scrape_user_stats("testuser")
            expected_stats = {
                "num_years": "3",
                "total_hours_watched": "150",
                "num_directors": "20",
                "num_countries": "8",
                "longest_streak_days": "10",
                "days_with_2_plus_films": "5",
            }
            self.assertEqual(stats, expected_stats)

    def test_scrape_user_stats_error_page(self):
        """Test scrape_user_stats returns empty dict when stats page has error."""
        def side_effect(url, **_kwargs):
            if url == "https://letterboxd.com/testuser/":
                return FakeResponse("<html><body><h1>Welcome</h1></body></html>", 200)
            if url == "https://letterboxd.com/testuser/stats":
                html = (
                    '<html><body class="error message-dark">'
                    "<h1>Letterboxd</h1>"
                    "<strong>Sorry, we can’t find the page you’ve requested.</strong>"
                    "</body></html>"
                )
                return FakeResponse(html, 200)
            return FakeResponse("", 404)

        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            mock_get.side_effect = side_effect
            stats = scrape_user_stats("testuser")
            self.assertEqual(stats, {})

    def test_scrape_user_stats_invalid_user(self):
        """Test scrape_user_stats raises ValueError for an invalid user."""
        with patch("src.helpers.scrapers_roast.requests.get") as mock_get:
            mock_get.return_value = FakeResponse("Not Found", 404)
            with self.assertRaises(ValueError):
                scrape_user_stats("nonexistentuser")


if __name__ == "__main__":
    unittest.main()
