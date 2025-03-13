"""
Scraper functions for extracting Letterboxd user details, reviews, and stats.
"""

import ast
import csv
import json
import re
from typing import List, Optional

import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import requests
import seaborn as sns
from bs4 import BeautifulSoup

# Define custom exception for scraper errors
class ScraperError(Exception):
    """Custom exception for scraper errors."""


def validate_letterboxd_user(username: str) -> bool:
    """
    Validate if a Letterboxd user exists.

    This function checks if the given username corresponds to a valid
    Letterboxd profile by fetching the profile URL and looking for error
    indicators in the page content.

    Parameters:
        username (str): The Letterboxd username.

    Returns:
        bool: True if the user profile is valid, False otherwise.
    """
    profile_url: str = f"https://letterboxd.com/{username}/"
    response = requests.get(profile_url)
    if response.status_code != 200:
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    error_h1 = soup.find("h1")
    error_strong = soup.find("strong")
    error_body = soup.find("body", class_="error message-dark")

    if (
        error_h1 and "Letterboxd" in error_h1.text
        and error_strong and "Sorry, we can’t find the page you’ve requested." in error_strong.text
        and error_body
    ):
        return False

    return True


def letterboxd_user_reviews_scraper(username: str) -> None:
    """
    Scrape and save a Letterboxd user's reviews to a CSV file.

    The function retrieves all review pages from the user's review section,
    extracts details such as movie name, URL, year, rating, watched date, and
    review text, and writes them into a CSV file named '{username}_reviews.csv'.

    Parameters:
        username (str): The Letterboxd username.

    Raises:
        ScraperError: If the user profile page cannot be retrieved.
    """
    base_profile_url: str = f"https://letterboxd.com/{username}"
    reviews_url: str = f"{base_profile_url}/films/reviews/"

    response = requests.get(reviews_url)
    if response.status_code != 200:
        raise ScraperError(
            f"Failed to get user profile from {base_profile_url}. "
            f"Status code: {response.status_code}"
        )

    soup = BeautifulSoup(response.text, "html.parser")
    page_links = soup.find_all("li", class_="paginate-page")
    last_page: int = 1
    if page_links:
        last_page = max(int(link.text) for link in page_links if link.text.isdigit())

    reviews: List[List[Optional[str]]] = []

    for page in range(1, last_page + 1):
        page_url: str = f"{base_profile_url}/films/reviews/page/{page}/"
        page_response = requests.get(page_url)
        if page_response.status_code != 200:
            continue

        page_soup = BeautifulSoup(page_response.text, "html.parser")
        review_elements = page_soup.find_all("div", class_="film-detail-content")

        for element in review_elements:
            # Extract movie name and URL
            movie_anchor = element.find("h2", class_="headline-2 prettify")
            movie_tag = movie_anchor.find("a") if movie_anchor else None
            movie_name: Optional[str] = movie_tag.text.strip() if movie_tag else None
            movie_url: Optional[str] = (
                f"https://letterboxd.com{movie_tag['href']}" if movie_tag and movie_tag.get("href") else None
            )

            # Extract movie year
            year_tag = element.find("small", class_="metadata")
            year_anchor = year_tag.find("a") if year_tag else None
            movie_year: Optional[str] = year_anchor.text.strip() if year_anchor else None

            # Extract rating
            rating_tag = element.find("span", class_="rating")
            rating: Optional[str] = rating_tag.text.strip() if rating_tag else None

            # Extract watched date
            date_tag = element.find("span", class_="date")
            watched_date: Optional[str] = (
                date_tag.text.replace("Watched", "").strip() if date_tag else None
            )

            # Extract review text
            review_tag = element.find("div", class_="js-review-body")
            review_text: Optional[str] = review_tag.get_text(strip=True) if review_tag else None

            reviews.append([
                movie_name,
                movie_url,
                movie_year,
                rating,
                watched_date,
                review_text,
            ])

    # Write the reviews data to a CSV file
    csv_filename: str = f"{username}_reviews.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Movie Name",
            "Movie URL",
            "Year",
            "Rating",
            "Watched Date",
            "Review"
        ])
        writer.writerows(reviews)


def letterboxd_user_stats_scraper(username: str) -> None:
    """
    Scrape and save a Letterboxd user's stats to a CSV file.

    The function fetches the user's stats page and extracts statistics such as
    number of years, total hours watched, number of directors, number of countries,
    longest streak, and days with 2+ films. The data is saved into a CSV file named
    '{username}_stats.csv'.

    Parameters:
        username (str): The Letterboxd username.

    Raises:
        ScraperError: If the stats page cannot be retrieved or if no stats are available.
    """
    stats_url: str = f"https://letterboxd.com/{username}/stats"
    response = requests.get(stats_url)
    if response.status_code != 200:
        raise ScraperError(f"Couldn't find stats for {username}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    error_h1 = soup.find("h1")
    error_strong = soup.find("strong")
    error_body = soup.find("body", class_="error message-dark")
    if (
        error_h1 and "Letterboxd" in error_h1.text
        and error_strong and "Sorry, we can’t find the page you’ve requested." in error_strong.text
        and error_body
    ):
        raise ScraperError(f"No stats available for {username}")

    stats_elements = soup.find_all("h4", class_="yir-member-statistic statistic")
    if len(stats_elements) < 6:
        raise ScraperError(f"Unexpected stats format for {username}")

    num_years: str = stats_elements[0].text.split()[0]
    num_hours: str = stats_elements[1].text.split()[0]
    num_directors: str = stats_elements[2].text.split()[0]
    num_countries: str = stats_elements[3].text.split()[0]
    longest_streak: str = stats_elements[4].text.split()[0]
    two_plus_film_days: str = stats_elements[5].text.split()[0]

    csv_filename: str = f"{username}_stats.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Number of Years",
            "Total Hours Watched",
            "Number of Directors",
            "Number of Countries",
            "Longest Streak (days)",
            "Days with 2+ Films"
        ])
        writer.writerow([
            num_years,
            num_hours,
            num_directors,
            num_countries,
            longest_streak,
            two_plus_film_days
        ])

