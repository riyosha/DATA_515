#!/usr/bin/env python3
"""
Letterboxd Roast Generator
This script generates a brutally funny roast based on a user's Letterboxd reviews
and stats using Google's Gemini API.
"""

import os
import sys
import pandas as pd
import google.generativeai as genai


def generate_funny_roast(username: str, api_key: str) -> None:
    """
    Generates a savage yet hilarious roast for a Letterboxd user based on their
    review data and stats.
    Args:
        username (str): Letterboxd username for file retrieval.
        api_key (str): API key for Google Gemini AI authentication.
    """
    # Configure the Gemini API with the provided API key
    genai.configure(api_key=api_key)

    reviews_file = f"{username}_reviews.csv"
    stats_file = f"{username}_stats.csv"

    try:
        reviews_df = pd.read_csv(reviews_file)
        reviews_text = reviews_df.to_string(index=False)

        stats_text = "No stats. Either a ghost or a cinematic criminal."
        if os.path.exists(stats_file):
            stats_df = pd.read_csv(stats_file)
            stats_text = stats_df.to_string(index=False)

        prompt = f"""
        You are a ruthlessly funny film critic. Roast this user's Letterboxd taste with quick, savage, 
        and hilarious burns. Keep it sharp, fast, and witty. Just pure cinematic destruction.
        
        - Open with a brutal one-liner about their taste.
        - Call out their worst takes—a classic they trashed or an embarrassing 5-star.
        - Mock their genre obsession—do they live in horror? Worship romcoms?
        - Drag their binge habits—Marvel cultist? Nicolas Cage devotee?
        - Roast their review style—one-word nonsense? Cringe poetry? Wikipedia summaries?
        - If stats exist, find the funniest thing (most-watched actor, absurd runtime, etc.).
        - End with a movie recommendation so painfully accurate it stings.
        
        ---
        Their Reviews: {reviews_text}
        Their Stats: {stats_text}
        
        Now, let them have it.
        """

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        print("\nYour Letterboxd Roast:\n")
        print(response.text)

    except FileNotFoundError:
        print(f"Error: Could not find file '{reviews_file}'. Make sure the username is correct.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{reviews_file}' is empty or not properly formatted.")
        sys.exit(1)
    except (ValueError, IOError) as error:
        print(f"Error processing files: {error}")
        sys.exit(1)
    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        sys.exit(1)


def get_api_key() -> str:
    """
    Retrieves the API key from environment variables.
    Returns:
        str: The API key for Gemini.
    Raises:
        EnvironmentError: If the API key is not found.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("API key not found. Please set GEMINI_API_KEY.")
    return api_key


def main() -> None:
    """Main function to run the Letterboxd roast generator."""
    api_key = get_api_key()
    username = input("Enter the Letterboxd username: ").strip()
    if not username:
        print("Error: Username cannot be empty.")
        sys.exit(1)
    generate_funny_roast(username, api_key)


if __name__ == "__main__":
    main()
