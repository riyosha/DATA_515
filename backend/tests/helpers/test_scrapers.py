"""Test suite for the Letterboxd scrapers.py helping functions"""

import unittest
from unittest import mock
from unittest.mock import patch, MagicMock


from src.helpers.scrapers import (
    validate_letterboxd_film_url,
    fetch_html_content,
    scrape_reviews,
    movie_details_scraper,
    ScraperError,
)


# Test suite for testing the Letterboxd scraper functionality
class TestLetterboxdScraper(unittest.TestCase):
    """Unit tests for the Letterboxd scraper functions."""

    def test_valid_url(self):
        """Test valid URL."""
        self.assertEqual(
            validate_letterboxd_film_url("https://letterboxd.com/film/the-brutalist/"),
            True,
        )

    def test_invalid_url(self):
        """Test invalid URL."""
        self.assertEqual(
            validate_letterboxd_film_url(
                "https://letterboxd.com/thediegoandaluz/film/the-brutalist/"
            ),
            False,
        )

    @patch("requests.get")
    def test_failed_http_request_fetch_html_content(self, mock_get):
        """Test fetch reviews when HTTP request fails."""
        valid_url = "https://letterboxd.com/film/moonfall/"
        mock_get.return_value.status_code = 404  # Simulating failed HTTP request
        headers = {"User-Agent": "Mozilla/5.0"}
        with self.assertRaises(ScraperError) as context:
            fetch_html_content(valid_url, headers)
        self.assertIn("Failed to get reviews", str(context.exception))

    @patch("requests.get")
    def test_fetch_html_content_success(self, mock_get):
        """Test fetch_html_content for a successful HTTP request."""

        # Mock the response object returned by requests.get
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Review Page</h1></body></html>"
        mock_get.return_value = mock_response

        url = "https://letterboxd.com/film/sample_movie/reviews/"
        headers = {"User-Agent": "Mozilla/5.0"}

        result = fetch_html_content(url, headers)

        # Assert that the mock GET request was made
        mock_get.assert_called_once_with(url, headers=headers, timeout=10)

        # Assert the response text is as expected
        self.assertEqual(result, "<html><body><h1>Review Page</h1></body></html>")

    @patch("src.helpers.scrapers.fetch_html_content")
    def test_scrape_reviews(self, mock_fetch_reviews):
        """Test scraping reviews from a Letterboxd page with n=2."""
        # Mocking the HTML response of the reviews pages
        mock_fetch_reviews.side_effect = [
            """
                <html>
                    <body>
                        <ul>
                            <li class="film-detail">
                                <div class="js-review-body">
                                    <p>Great movie!</p>
                                </div>
                                <div class="rating">5/5</div>
                            </li>
                            <li class="film-detail">
                                <div class="rating">3/5</div>
                            </li>
                        </ul>
                    </body>
                </html>
            """,
            """
                <html>
                    <body>
                        <ul>
                            <li class="film-detail">
                                <div class="js-review-body">
                                    <p>Amazing film!</p>
                                </div>
                                <div class="rating">4/5</div>
                            </li>
                            <li class="film-detail">
                                <div class="js-review-body">
                                    <p>Could have been more exciting.</p>
                                </div>
                                <div class="rating">2/5</div>
                            </li>
                        </ul>
                    </body>
                </html>
            """,
        ]

        reviews = scrape_reviews("https://letterboxd.com/film/some-movie/", n=2)

        # Assert that a total of 4 reviews are scraped (2 reviews from each page)
        self.assertEqual(len(reviews), 4)
        self.assertEqual(reviews[0]["review_text"], "Great movie!")
        self.assertEqual(reviews[0]["rating"], "5/5")
        self.assertEqual(reviews[1]["review_text"], "")
        self.assertEqual(reviews[1]["rating"], "3/5")
        self.assertEqual(reviews[2]["review_text"], "Amazing film!")
        self.assertEqual(reviews[2]["rating"], "4/5")
        self.assertEqual(reviews[3]["review_text"], "Could have been more exciting.")
        self.assertEqual(reviews[3]["rating"], "2/5")

    @patch("src.helpers.scrapers.fetch_html_content")
    def test_scrape_reviews_no_reviews(self, mock_fetch_reviews):
        """Test if no reviews are found."""
        mock_fetch_reviews.return_value = """
            <html>
                <body>
                    <ul>
                        <!-- No reviews available -->
                    </ul>
                </body>
            </html>
        """
        reviews = scrape_reviews("https://letterboxd.com/film/some-movie/", n=1)
        self.assertEqual(len(reviews), 0)  # No reviews

    def test_scrape_reviews_invalid_url(self):
        """Test for invalid url"""
        with self.assertRaises(ValueError):
            scrape_reviews("https://letterboxd.com/INVALID", n=1)

    @patch("src.helpers.scrapers.fetch_html_content")
    def test_scrape_reviews_fetch_failure(self, mock_fetch_reviews):
        """Test handling of fetch_reviews failure in scrape_reviews."""
        mock_fetch_reviews.side_effect = ScraperError("Failed to get reviews")

        reviews = scrape_reviews("https://letterboxd.com/film/some-movie/", n=1)

        self.assertEqual(len(reviews), 0)

    @patch("requests.get")
    def test_movie_details_scraper_success(self, mock_get):
        """Test scraping movie details including movie name."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <h1 class="headline-1 filmtitle">
                    <span class="name js-widont prettify">Some Movie</span>
                </h1>
                <div class="releaseyear"><a>2025</a></div>
                <span class="directorlist">John Doe</span>
                <div id="tab-genres">
                    <span class="text-slug">Drama</span>
                    <span class="text-slug">Action</span>
                </div>
                <div class="truncate">
                    <p>A thrilling action movie.</p>
                </div>
                <div id="backdrop" data-backdrop="http://example.com/backdrop.jpg"></div>
            </html>
        """
        mock_get.return_value = mock_response

        details = movie_details_scraper("https://letterboxd.com/film/some-movie/")

        self.assertEqual(details["movie_name"], "Some Movie")  # Updated to match extracted name
        self.assertEqual(details["year"], "2025")
        self.assertEqual(details["director"], "John Doe")
        self.assertEqual(details["genres"], "Drama, Action")
        self.assertEqual(details["synopsis"], "A thrilling action movie.")
        self.assertEqual(details["backdrop_image_url"], "http://example.com/backdrop.jpg")

    @patch("requests.get")
    def test_movie_details_scraper_failure(self, mock_get):
        """Test scraping movie details when data is missing."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <!-- Missing all expected elements -->
                <!-- No release year, no director, no genres, no synopsis, and no backdrop -->
            </html>
        """
        mock_get.return_value = mock_response

        details = movie_details_scraper("https://letterboxd.com/film/some-movie/")

        # Test if the missing data returns None or empty values as expected
        self.assertEqual(details["movie_name"], None)
        self.assertEqual(details["year"], None)
        self.assertEqual(details["director"], None)
        self.assertEqual(details["genres"], None)
        self.assertEqual(details["synopsis"], None)
        self.assertEqual(details["backdrop_image_url"], None)

    def test_movie_details_scraper_invalid_url(self):
        """Test for invalid url"""
        with self.assertRaises(ValueError):
            movie_details_scraper("https://letterboxd.com/INVALID")


# Running the tests
if __name__ == "__main__":
    unittest.main()
