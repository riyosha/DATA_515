"""
Module containing functions for generating a savage roast based on
Letterboxd user reviews and statistics.
"""

import google.generativeai as genai


class RoastGenerationError(Exception):
    """Custom exception for roast generation errors."""


class LetterboxdRoastAnalyzer:
    """
    A class for analyzing Letterboxd user reviews and statistics to generate a
    brutally funny roast using an AI model.
    """

    SAFETY_SETTINGS = [
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

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

        reviews_text = " >>> ".join(
            element["review_text"]
            for element in reviews_list
            if "review_text" in element
        )

        if not stats_dict:
            stats_text = "No statistics available."
        else:
            stats_lines = []
            for key, value in stats_dict.items():
                stats_lines.append(f"{key.replace('_', ' ').title()}: {value}")
            stats_text = "\n".join(stats_lines)

        combined_text = (
            f"User Reviews:\n{reviews_text}\n\nUser Statistics:\n{stats_text}\n"
        )
        return combined_text

    def generate_roast(self, user_data, api_key, safety="off"):
        """
        Generates a savage roast using the provided user data.

        Args:
            user_data (str): The combined reviews and stats text.
            api_key (str): The API key for the AI model.
            safety (str, optional): Safety mode for content generation.
                Defaults to 'off'.

        Returns:
            str: The generated roast.

        Raises:
            RoastGenerationError: If the roast is too long or an error occurs.
        """
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = (
            "\nYou are a ruthlessly funny film critic. Based solely on the following "
            "user reviews and statistics, generate a savage, witty, and brutally honest "
            "roast that skewers the user's cinematic taste and habits. Use humor and sharp "
            "insights, but avoid overly offensive language.\n\n"
            f"{user_data}\n\n"
            "Additionally, for each movie, compute the difference between the user's rating "
            "and the movie's average rating. Let:\n  - guilty_pleasure_movie = maximum "
            "difference,\n  - unpopular_opinion = minimum difference.\n\n"
            "Then, incorporate these observations:\n  - If guilty_pleasure_movie is less "
            "than 2 and unpopular_opinion is greater than -2, add: "
            "\"You are basic and have no original thoughts.\"\n  - If guilty_pleasure_movie "
            "is greater than or equal to 2, ask: \"Do you really like that movie?\"\n  - If "
            "unpopular_opinion is greater than -2, add: "
            "\"You are alone on this one, everyone likes this movie, bro.\"\n\n"
            "Ensure the roast is concise and impactful. Keep it strictly under 500 words in "
            "5-7 steps."
        )

        if safety == "off":
            prompt += "\n- Do not generate publicly offensive language."

        response = model.generate_content(
            prompt, safety_settings=self.SAFETY_SETTINGS
        )
        roast = response.text

        if len(roast.split()) > 710:
            raise RoastGenerationError("Roast generated is too long.")

        return roast

    def get_results(self, reviews_list, stats_dict, api_keys, safety="off"):
        """
        Generates the final roast by combining reviews and stats, and calling the AI
        model using multiple API keys if needed.

        Args:
            reviews_list (list): A list of review dictionaries.
            stats_dict (dict): A dictionary containing user statistics.
            api_keys (list): A list of API keys for generating the roast.
            safety (str, optional): Safety mode for content generation.
                Defaults to 'off'.

        Returns:
            str: The generated roast.

        Raises:
            RoastGenerationError: If roast generation fails after multiple attempts.
        """
        user_data = self.read_user_data(reviews_list, stats_dict)
        roast = None
        for i, key in enumerate(api_keys):
            try:
                roast = self.generate_roast(user_data, key, safety=safety)
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
