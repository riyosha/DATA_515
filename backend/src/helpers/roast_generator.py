"""
Module containing functions for generating a savage roast based on Letterboxd
user reviews and statistics.
"""

import google.generativeai as genai


class RoastGenerationError(Exception):
    """Custom exception for roast generation errors."""


class LetterboxdRoastAnalyzer:
    """
    A class for analyzing Letterboxd user reviews and statistics to generate a
    brutally funny roast using an AI model.
    """

    def read_user_data(self, reviews_list, stats_dict):
        """
        Reads reviews and statistics, and formats them into a single string.

        Args:
            reviews_list (list): A list of dictionaries, each containing a
                'review_text' key.
            stats_dict (dict): A dictionary containing user statistics.

        Returns:
            str: A string that combines all reviews and stats for prompt
                generation.

        Raises:
            ValueError: If reviews_list is empty.
        """
        if not reviews_list:
            raise ValueError("No reviews provided.")

        # Combine reviews by joining each review_text with a delimiter.
        reviews_text = " >>> ".join(
            element["review_text"]
            for element in reviews_list
            if "review_text" in element
        )

        # Format stats into a neat string; if no stats provided, use a default message.
        if not stats_dict:
            stats_text = "No statistics available."
        else:
            stats_lines = []
            for key, value in stats_dict.items():
                stats_lines.append(f"{key.replace('_', ' ').title()}: {value}")
            stats_text = "\n".join(stats_lines)

        # Combine the reviews and stats into one string.
        combined_text = (
            f"User Reviews:\n{reviews_text}\n\nUser Statistics:\n{stats_text}\n"
        )
        return combined_text

    def generate_roast(self, user_data, api_key):
        """
        Generates a savage roast using the provided user data.

        Args:
            user_data (str): The combined reviews and stats text.
            api_key (str): The API key for the AI model.

        Returns:
            str: The generated roast.

        Raises:
            RoastGenerationError: If the roast is too long or an error occurs.
        """
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f""" You're a ruthless, wildly funny film critic, and your job is to
                      obliterate this user's Letterboxd taste in a way that's fast, savage,
                      and impossible to ignore. No lists, no formatting—just a single,
                      flowing paragraph that roasts them so brutally they’ll question
                      every movie they've ever watched.

                      Here are their reviews , ratings and their stats:{user_data}

                      Now, open with a devastating one-liner about their taste, then
                      tear apart their worst ratings—mock the classic they unfairly
                      trashed or the embarrassing five-star they handed out. Drag their
                      genre obsession—do they live in horror? Worship romcoms? Are they
                      trapped in an endless Marvel marathon? Make fun of their binge 
                      habits—if their most-watched actor or director is absurdly specific
                      or tragic, call it out. If they have a weirdly high watch count for a
                      single film, expose them. Roast their review style—whether they write
                      pretentious essays, cryptic one-word takes, or full-on Wikipedia summaries.
                      End by recommending a movie so painfully accurate it stings without using **,
                      the kind of film that perfectly sums up their questionable taste.

                      Absolutely no bold text and dont use ** ** ever, no bullet points, no structured
                      formatting—just a single, natural-flowing paragraph like a real, brutal, hilarious
                      film critique. Do not use Markdown, asterisks, or any formatting characters—output
                      must be plain text only.
                  """

        response = model.generate_content(prompt)
        roast = response.text

        if len(roast.split()) > 710:
            raise RoastGenerationError("Roast generated is too long.")

        return roast

    def get_results(self, reviews_list, stats_dict, api_keys):
        """
        Generates the final roast by combining reviews and stats, and calling the AI
        model using multiple API keys if needed.

        Args:
            reviews_list (list): A list of review dictionaries.
            stats_dict (dict): A dictionary containing user statistics.
            api_keys (list): A list of API keys for generating the roast.

        Returns:
            str: The generated roast.

        Raises:
            RoastGenerationError: If roast generation fails after multiple attempts.
        """
        user_data = self.read_user_data(reviews_list, stats_dict)
        roast = None
        for i, key in enumerate(api_keys):
            try:
                roast = self.generate_roast(user_data, key)
                if roast and roast.strip():
                    break
            except Exception as error:  # pylint: disable=broad-exception-caught
                print(f"Error generating roast with API key {i}: {error}")
                continue
        else:
            raise RoastGenerationError(
                "Failed to generate roast after multiple attempts."
            )

        return roast
