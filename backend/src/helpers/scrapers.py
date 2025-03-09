"""
Scraper functions for extracting movie details and reviews from Letterboxd.
"""

import re
import requests
from bs4 import BeautifulSoup


class ScraperError(Exception):
    """Custom exception for scraper errors."""


def validate_letterboxd_film_url(film_url):
    """Validates the Letterboxd film URL."""
    pattern = r"^https://letterboxd\.com/film/[\w-]+/$"
    return bool(re.match(pattern, film_url))


def fetch_reviews(url, headers):
    """Fetches HTML content from a given URL."""
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return response.text
    raise ScraperError(
        f"Failed to get reviews from {url}. Status code: {response.status_code}"
    )


def scrape_reviews(film_url, n=30):
    """Scrapes reviews from a Letterboxd movie page."""
    if not validate_letterboxd_film_url(film_url):
        raise ValueError(f"Invalid URL: {film_url}")

    headers = {"User-Agent": "Mozilla/5.0"}

    reviews_data = []

    for page in range(1, n + 1):
        html_content = fetch_reviews(
            f"{film_url}reviews/by/activity/page/{page}/", headers
        )
        soup = BeautifulSoup(html_content, "html.parser")
        reviews = soup.select("li.film-detail")

        for review in reviews:
            review_text = review.select_one(".js-review-body p")
            rating = review.select_one(".rating")
            reviews_data.append({
                "rating": rating.get_text(strip=True) if rating else "No Rating",
                "review_text": review_text.get_text(strip=True) if review_text else "",
            })

    return reviews_data


def movie_details_scraper(url):
    """Scrapes movie details and backdrop image from Letterboxd."""
    if not validate_letterboxd_film_url(url):
        raise ValueError(f"Invalid URL: {url}")

    movie_name = url.split("/")[-2]
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise ScraperError(
            f"Failed to retrieve details from {url}. Status code: {response.status_code}"
        )

    soup = BeautifulSoup(response.text, "html.parser")

    def extract_text(selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None

    year = extract_text("div.releaseyear a")
    director = extract_text("span.directorlist")
    genres = ", ".join(
        [g.get_text(strip=True) for g in soup.select("#tab-genres .text-slug")]
    )
    genres = genres.replace(" Show All…", "")
    synopsis = extract_text(".truncate p")

    movie_details = {
        "movie_name": movie_name,
        "year": year,
        "director": director,
        "genres": genres,
        "synopsis": synopsis
    }

    # Extract backdrop image URL (if any)
    backdrop_url = soup.select_one("#backdrop[data-backdrop]")
    if backdrop_url:
        backdrop_image_url = backdrop_url["data-backdrop"]
    else:
        backdrop_image_url = None

    movie_details["backdrop_image_url"] = backdrop_image_url

    return movie_details
