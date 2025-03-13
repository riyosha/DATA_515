import requests
from bs4 import BeautifulSoup
import csv
import ast
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import google.generativeai as genai
import csv
import re

def validate_letterboxd_user(username):

    profile_url = f'https://letterboxd.com/{username}/'
    response = requests.get(profile_url)
    if response.status_code != 200:
        return False
    elif response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        error_h1 = soup.find("h1")
        error_strong = soup.find("strong")
        error_body = soup.find("body", class_="error message-dark")

        if error_h1 and "Letterboxd" in error_h1.text and error_strong and "Sorry, we can’t find the page you’ve requested." in error_strong.text and error_body:
            return False
        else:
            return True


def letterboxd_user_reviews_scraper(username):

    profile_url = f'https://letterboxd.com/{username}/'

    response = requests.get(profile_url+'/films/reviews/')
    if response.status_code != 200:
        raise ScraperError(f"Failed to get user profile from {profile_url}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    page_links = soup.find_all("li", class_="paginate-page")
    last_page = 1
    if page_links:
        last_page = max(int(link.text) for link in page_links if link.text.isdigit())



    reviews = []

    for i in range(1, last_page + 1):

        _url = f"{profile_url}/films/reviews/page/{i}/"
        _response = requests.get(_url)

        if _response.status_code != 200:
            pass

        _soup = BeautifulSoup(_response.text, "html.parser")

        for element in _soup.find_all("div", class_="film-detail-content"):
            # Extract movie name and URL
            movie_tag = element.find("h2", class_="headline-2 prettify").find("a")
            movie_name = movie_tag.text.strip() if movie_tag else None
            movie_url = f"https://letterboxd.com{movie_tag['href']}" if movie_tag else None

            # Extract movie year
            year_tag = element.find("small", class_="metadata").find("a")
            movie_year = year_tag.text.strip() if year_tag else None

            # Extract rating
            rating_tag = element.find("span", class_="rating")
            rating = rating_tag.text.strip() if rating_tag else None

            # Extract watched date
            date_tag = element.find("span", class_="date")
            watched_date = date_tag.text.replace("Watched", "").strip() if date_tag else None

            # Extract review text
            review_tag = element.find("div", class_="js-review-body")
            review_text = review_tag.get_text(strip=True) if review_tag else None

            # Store the extracted data
            reviews.append([
                            movie_name, movie_url, movie_year, rating, watched_date, review_text
            ])

        with open(f'{username}_reviews.csv', mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Movie Name", "Movie URL", "Year", "Rating", "Watched Date", "Review"])
            writer.writerows(reviews)



# takes about 1s per page to extract reviews


def letterboxd_user_stats_scraper(username):
    stats_url = f'https://letterboxd.com/{username}/stats'

    response = requests.get(stats_url)
    if response.status_code != 200:
        raise ScraperError(f"Couldn't find stats for {username}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        error_h1 = soup.find("h1")
        error_strong = soup.find("strong")
        error_body = soup.find("body", class_="error message-dark")

        if error_h1 and "Letterboxd" in error_h1.text and error_strong and "Sorry, we can’t find the page you’ve requested." in error_strong.text and error_body:
            raise SraperError(f"No stats available for {username}" )
        else:


            soup = BeautifulSoup(response.text, 'html.parser')

            stats = soup.find_all('h4', class_="yir-member-statistic statistic")

            num_years = stats[0].text.split()[0]
            num_hours = stats[1].text.split()[0]
            num_directors = stats[2].text.split()[0]
            num_countries = stats[3].text.split()[0]
            longest_streak = stats[4].text.split()[0]
            two_plus_film_days = stats[5].text.split()[0]

            with open(f'{username}_stats.csv', mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Number of Years", "Total Hours Watched", "Number of Directors",
                                 "Number of Countries", "Longest Streak (days)", "Days with 2+ Films"])
                writer.writerow([num_years, num_hours, num_directors, num_countries, longest_streak, two_plus_film_days])
# Prompt user for Letterboxd username
username = input("Enter Letterboxd username: ").strip()

print(f"Scraping data for '{username}'...")

# Scrape user reviews
try:
    letterboxd_user_reviews_scraper(username)
    print(f"Reviews scraped and saved as '{username}_reviews.csv'")
except Exception as e:
    print(f"Error scraping reviews: {e}")

# Scrape user stats
try:
    letterboxd_user_stats_scraper(username)
    print(f"Stats scraped and saved as '{username}_stats.csv'")
except Exception as e:
    print(f"Error scraping stats: {e}")

print("Scraping completed successfully!")
import google.generativeai as genai
import pandas as pd
import os

# Configure Gemini API 
genai.configure(api_key="API_key")

# Function to find and process the user's CSV files
def process_letterboxd_data(username):
    reviews_file = f"{username}_reviews.csv"
    stats_file = f"{username}_stats.csv"

    # Check if both files exist
    if not os.path.exists(reviews_file) or not os.path.exists(stats_file):
        print(f"Error: One or both files for {username} are missing!")
        return None

    try:
        # Load CSV files
        reviews_df = pd.read_csv(reviews_file)
        stats_df = pd.read_csv(stats_file)

        # Extract total reviews
        total_reviews = len(reviews_df)

        # Most common movie year
        most_common_year = reviews_df['Year'].mode()[0] if 'Year' in reviews_df.columns else "Unknown"

        # Average rating (if ratings exist)
        if 'Rating' in reviews_df.columns:
            ratings = pd.to_numeric(reviews_df['Rating'], errors='coerce')
            avg_rating = round(ratings.mean(), 2) if not ratings.isnull().all() else "Unknown"
        else:
            avg_rating = "Unknown"

        # Extract stats dynamically
        stats_summary = stats_df.to_dict(orient="records")[0]

        # === Funny & Creative Enhancements ===

        # Movie-watching addiction humor
        watch_streak = stats_summary.get("Longest Streak (days)", "Unknown")
        if "w" in str(watch_streak):
            watch_streak = f"{watch_streak} (which means you spent {watch_streak.split('w')[0]} WEEKS doing nothing but watching movies.)"

        # Hours watched exaggeration
        total_hours = stats_summary.get("Total Hours Watched", "Unknown")
        if total_hours != "Unknown":
            total_days = round(int(total_hours.replace(",", "")) / 24, 1)
            total_hours = f"{total_hours} hours (~{total_days} DAYS straight of movies—are you okay?)"

        # Unique directors roasting
        num_directors = stats_summary.get("Number of Directors", "Unknown")
        if num_directors != "Unknown":
            num_directors = f"{num_directors} different directors (or do you just keep rewatching Tarantino?)"

        # Country diversity joke
        num_countries = stats_summary.get("Number of Countries", "Unknown")
        if num_countries != "Unknown":
            if int(num_countries) > 50:
                num_countries = f"{num_countries} countries—impressive, but let’s be real, it's mostly Hollywood."
            else:
                num_countries = f"{num_countries} countries. A *bit* of variety, but still probably 90% English films."

        return {
            "Total Reviews": f"{total_reviews} movies (do you even have hobbies?)",
            "Most Common Year": f"{most_common_year} (Is this your whole personality?)",
            "Average Rating": f"{avg_rating} (So do you like movies, or just enjoy suffering?)",
            "Stats Summary": {
                "Total Hours Watched": total_hours,
                "Unique Directors Watched": num_directors,
                "Countries Represented": num_countries,
                "Longest Streak": watch_streak,
                "Days with 2+ Movies Watched": stats_summary.get("Days with 2+ Films", "Unknown")
            }
        }

    except Exception as e:
        print(f"Error processing Letterboxd data: {e}")
        return None

# Function to generate a funny roast
def generate_funny_roast(username):
    insights = process_letterboxd_data(username)

    if insights is None:
        return

    # Construct a humorous roast prompt
    prompt = f"""
    You are a sarcastic yet witty movie critic. Based on the user's Letterboxd reviews and stats,
    create a **funny and witty 5-7 line roast**.

    Here’s their **movie-watching profile**:

    - **Total Reviews:** {insights["Total Reviews"]}
    - **Most Watched Year:** {insights["Most Common Year"]}
    - **Average Rating:** {insights["Average Rating"]}
    - **User Stats:**
      - **Total Hours Watched:** {insights["Stats Summary"]["Total Hours Watched"]}
      - **Unique Directors Watched:** {insights["Stats Summary"]["Unique Directors Watched"]}
      - **Countries Represented:** {insights["Stats Summary"]["Countries Represented"]}
      - **Longest Streak:** {insights["Stats Summary"]["Longest Streak"]}
      - **Days with 2+ Movies Watched:** {insights["Stats Summary"]["Days with 2+ Movies Watched"]}

    Be **playfully sarcastic but not mean**. Call them out on their **weird film choices**,
    their binge-watching habits, and anything absurd in their stats.
    Make fun of their **obsession with a particular movie year**, long streaks, or excessive ratings.
    Keep it **fun and entertaining**.

    Now, let the roasting begin! 😂🔥
    """

    # Call Gemini 1.5 Pro model
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

        # Print the funny roast
        print("\n🔥 Your Letterboxd Roast 🔥\n")
        print(response.text)

    except Exception as e:
        print(f"Error generating roast: {e}")

# Run the roast generator (Dynamically picks up any user's data)
username = input("Enter the Letterboxd username: ").strip()
generate_funny_roast(username)

