"""Scraper module for Letterboxd user profiles."""

import requests
from bs4 import BeautifulSoup


class ScraperError(Exception):
    """Custom exception for scraper errors."""


def validate_letterboxd_user(username):
    """
    Validates the Letterboxd user profile by checking if it exists.

    Args:
        username (str): The Letterboxd username.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    profile_url = f"https://letterboxd.com/{username}/"
    try:
        response = requests.get(profile_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except Exception as e:
        raise ScraperError(f"Error fetching {profile_url}: {e}") from e
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    error_h1 = soup.find("h1")
    error_strong = soup.find("strong")
    error_body = soup.find("body", class_="error message-dark")
    if error_h1 and error_strong and error_body:
        if (
            "Letterboxd" in error_h1.get_text()
            and "Sorry, we can’t find the page you’ve requested." in error_strong.get_text()
        ):
            return False
    return True


def fetch_html_content(url, headers):
    """
    Fetches HTML content from a given URL.

    Args:
        url (str): The URL to fetch.
        headers (dict): HTTP headers to use.

    Returns:
        str: HTML content.

    Raises:
        ScraperError: If fetching the URL fails.
    """
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return response.text
    raise ScraperError(f"Failed to fetch {url}. Status code: {response.status_code}")


def _parse_review_element(element):
    """
    Parses a review element from Letterboxd and returns a dictionary of review details.

    Args:
        element (bs4.element.Tag): A BeautifulSoup Tag representing a review element.

    Returns:
        dict: Parsed review details.
    """
    header = element.find("h2", class_="headline-2 prettify")
    movie_tag = header.find("a") if header else None
    movie_name = movie_tag.get_text(strip=True) if movie_tag else None
    movie_url = (
        f"https://letterboxd.com{movie_tag['href']}"
        if movie_tag and movie_tag.get("href")
        else None
    )
    metadata = element.find("small", class_="metadata")
    year_tag = metadata.find("a") if metadata else None
    movie_year = year_tag.get_text(strip=True) if year_tag else None
    rating_tag = element.find("span", class_="rating")
    rating = rating_tag.get_text(strip=True) if rating_tag else None
    date_tag = element.find("span", class_="date")
    watched_date = (
        date_tag.get_text(strip=True).replace("Watched", "").strip()
        if date_tag
        else None
    )
    review_tag = element.find("div", class_="js-review-body")
    review_text = review_tag.get_text(strip=True) if review_tag else ""
    return {
        "movie_name": movie_name,
        "movie_url": movie_url,
        "movie_year": movie_year,
        "rating": rating,
        "watched_date": watched_date,
        "review_text": review_text,
    }


def scrape_user_reviews(username, n_pages=10):
    """
    Scrapes user reviews from a Letterboxd profile.

    Args:
        username (str): The Letterboxd username.
        n_pages (int): Maximum number of review pages to scrape.

    Returns:
        list: A list of dictionaries, each containing details of a review.

    Raises:
        ValueError: If the user profile is invalid.
    """
    if not validate_letterboxd_user(username):
        raise ValueError(f"Invalid or non-existent user profile: {username}")

    base_url = f"https://letterboxd.com/{username}/films/reviews/"
    soup = BeautifulSoup(fetch_html_content(base_url, {"User-Agent": "Mozilla/5.0"}), "html.parser")
    try:
        last_page = max(
            int(link.get_text()) for link in soup.find_all("li", class_="paginate-page")
            if link.get_text().isdigit()
        ) if soup.find_all("li", class_="paginate-page") else 1
    except ValueError:
        last_page = 1

    reviews = []
    for page in range(1, min(n_pages, last_page) + 1):
        page_url = f"{base_url}page/{page}/"
        try:
            page_soup = BeautifulSoup(
                fetch_html_content(page_url, {"User-Agent": "Mozilla/5.0"}), "html.parser"
            )
        except ScraperError:
            continue
        for element in page_soup.find_all("div", class_="film-detail-content"):
            reviews.append(_parse_review_element(element))
    return reviews


def scrape_user_stats(username):
    """
    Scrapes user statistics from a Letterboxd profile.

    Args:
        username (str): The Letterboxd username.

    Returns:
        dict: A dictionary containing user statistics, or an empty dict if the stats
              page is not available.
    """
    if not validate_letterboxd_user(username):
        raise ValueError(f"Invalid or non-existent user profile: {username}")

    stats_url = f"https://letterboxd.com/{username}/stats"
    try:
        html_content = fetch_html_content(stats_url, {"User-Agent": "Mozilla/5.0"})
    except ScraperError:
        return {}

    soup = BeautifulSoup(html_content, "html.parser")
    error_h1 = soup.find("h1")
    error_strong = soup.find("strong")
    error_body = soup.find("body", class_="error message-dark")
    if error_h1 and error_strong and error_body:
        return {}

    stats_elements = soup.find_all("h4", class_="yir-member-statistic statistic")
    keys = [
        "num_years",
        "total_hours_watched",
        "num_directors",
        "num_countries",
        "longest_streak_days",
        "days_with_2_plus_films",
    ]
    stats_dict = {}
    for i, key in enumerate(keys):
        if i < len(stats_elements):
            stats_dict[key] = stats_elements[i].get_text(strip=True).split()[0]
        else:
            stats_dict[key] = None
    return stats_dict
