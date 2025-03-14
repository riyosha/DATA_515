"""
Test suite for the scrapers_roast.py helper functions.
"""

import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.helpers.scrapers_roast import (
    validate_letterboxd_user,
    letterboxd_user_reviews_scraper,
    letterboxd_user_stats_scraper,
    ScraperError,
)


class TestLetterboxdScrapersRoast(unittest.TestCase):
    """Unit tests for the Letterboxd scrapers_roast functions."""

    @patch("src.helpers.scrapers_roast.requests.get")
    def test_validate_letterboxd_user_valid(self, mock_get):
        """Test that a valid user returns True."""
        html_content = """
        <html>
            <body>
                <h1>Welcome to Letterboxd</h1>
            </body>
        </html>
        """
        mock_response = MagicMock(status_code=200, text=html_content)
        mock_get.return_value = mock_response

        result = validate_letterboxd_user("validuser")
        self.assertTrue(result)

    @patch("src.helpers.scrapers_roast.requests.get")
    def test_validate_letterboxd_user_invalid_http(self, mock_get):
        """Test that a non-200 HTTP response returns False."""
        mock_response = MagicMock(status_code=404, text="Not Found")
        mock_get.return_value = mock_response

        result = validate_letterboxd_user("nonexistentuser")
        self.assertFalse(result)

    @patch("src.helpers.scrapers_roast.requests.get")
    def test_validate_letterboxd_user_invalid_error_markers(self, mock_get):
        """Test that a 200 response with error markers returns False."""
        error_html = """
        <html>
            <body class="error message-dark">
                <h1>Letterboxd Error</h1>
                <strong>Sorry, we can't find the page you've requested.</strong>
            </body>
        </html>
        """
        mock_response = MagicMock(status_code=200, text=error_html)
        mock_get.return_value = mock_response

        result = validate_letterboxd_user("nonexistentuser")
        self.assertFalse(result)

    @patch("src.helpers.scrapers_roast.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_letterboxd_user_reviews_scraper_success(self, mock_file, mock_get):
        """Test that user reviews are scraped and saved to a CSV file."""
        # Simulate the reviews overview page with pagination links
        overview_html = """
        <html>
            <body>
                <ul>
                    <li class="paginate-page">1</li>
                    <li class="paginate-page">2</li>
                </ul>
            </body>
        </html>
        """
        # Simulate review page for page 1
        page1_html = """
        <html>
            <body>
                <div class="film-detail-content">
                    <h2 class="headline-2 prettify">
                        <a href="/film/movie1/">Movie One</a>
                    </h2>
                    <small class="metadata"><a>2020</a></small>
                    <span class="rating">4/5</span>
                    <span class="date">Watched 2021-01-01</span>
                    <div class="js-review-body">Great movie!</div>
                </div>
            </body>
        </html>
        """
        # Simulate review page for page 2
        page2_html = """
        <html>
            <body>
                <div class="film-detail-content">
                    <h2 class="headline-2 prettify">
                        <a href="/film/movie2/">Movie Two</a>
                    </h2>
                    <small class="metadata"><a>2019</a></small>
                    <span class="rating">3/5</span>
                    <span class="date">Watched 2021-02-01</span>
                    <div class="js-review-body">Not bad.</div>
                </div>
            </body>
        </html>
        """

        # Setup side effects for requests.get:
        # First call returns the overview page, then review pages for page 1 and 2.
        mock_get.side_effect = [
            MagicMock(status_code=200, text=overview_html),
            MagicMock(status_code=200, text=page1_html),
            MagicMock(status_code=200, text=page2_html),
        ]

        letterboxd_user_reviews_scraper("testuser")

        # Verify that the CSV file was opened for writing
        mock_file.assert_called_with(
            "testuser_reviews.csv",
            mode="w",
            newline="",
            encoding="utf-8"
        )
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        # Check for CSV header and expected data rows.
        self.assertIn("Movie Name,Movie URL,Year,Rating,Watched Date,Review", written_content)
        self.assertIn(
            "Movie One,https://letterboxd.com/film/movie1/,2020,4/5,2021-01-01,Great movie!",
            written_content
        )
        self.assertIn(
            "Movie Two,https://letterboxd.com/film/movie2/,2019,3/5,2021-02-01,Not bad.",
            written_content
        )

    @patch("src.helpers.scrapers_roast.requests.get")
    def test_letterboxd_user_reviews_scraper_http_failure(self, mock_get):
        """Test that reviews scraper raises an error when the initial HTTP request fails."""
        mock_get.return_value = MagicMock(status_code=404, text="Not Found")
        with self.assertRaises(ScraperError):
            letterboxd_user_reviews_scraper("testuser")

    @patch("src.helpers.scrapers_roast.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_letterboxd_user_stats_scraper_success(self, mock_file, mock_get):
        """Test that user stats are scraped and saved to a CSV file."""
        # Simulate a valid stats page HTML containing six stat elements
        stats_html = """
        <html>
            <body>
                <h4 class="yir-member-statistic statistic">5 years</h4>
                <h4 class="yir-member-statistic statistic">100 hours</h4>
                <h4 class="yir-member-statistic statistic">50 directors</h4>
                <h4 class="yir-member-statistic statistic">20 countries</h4>
                <h4 class="yir-member-statistic statistic">30 days</h4>
                <h4 class="yir-member-statistic statistic">10 days</h4>
            </body>
        </html>
        """
        mock_get.return_value = MagicMock(status_code=200, text=stats_html)

        letterboxd_user_stats_scraper("testuser")

        # Verify that the CSV file was opened for writing.
        mock_file.assert_called_with(
            "testuser_stats.csv",
            mode="w",
            newline="",
            encoding="utf-8"
        )
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        # Check for CSV header and expected stats row.
        self.assertIn(
            "Number of Years,Total Hours Watched,Number of Directors,"
            "Number of Countries,Longest Streak (days),Days with 2+ Films",
            written_content,
        )
        self.assertIn("5,100,50,20,30,10", written_content)

    @patch("src.helpers.scrapers_roast.requests.get")
    def test_letterboxd_user_stats_scraper_http_failure(self, mock_get):
        """Test that stats scraper raises an error when the stats page HTTP request fails."""
        mock_get.return_value = MagicMock(status_code=404, text="Not Found")
        with self.assertRaises(ScraperError):
            letterboxd_user_stats_scraper("testuser")

    @patch("src.helpers.scrapers_roast.requests.get")
    def test_letterboxd_user_stats_scraper_error_markers(self, mock_get):
        """Test that stats scraper raises an error when error markers are present in the HTML."""
        error_html = """
        <html>
            <body class="error message-dark">
                <h1>Letterboxd Error</h1>
                <strong>Sorry, we can't find the page you've requested.</strong>
            </body>
        </html>
        """
        mock_get.return_value = MagicMock(status_code=200, text=error_html)
        with self.assertRaises(ScraperError):
            letterboxd_user_stats_scraper("testuser")


if __name__ == "__main__":
    unittest.main()
