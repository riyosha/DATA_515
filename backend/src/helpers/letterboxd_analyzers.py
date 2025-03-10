"""File containing functions for generating a summary and aspects from reviews"""

import json
import re
import ast
import google.generativeai as genai


class AspectFormatError(Exception):
    """Custom exception for aspect format errors."""


class SummaryError(Exception):
    """Custom exception for summary format errors."""


class LetterboxdReviewAnalyzer:
    """A class for analyzing Letterboxd movie reviews using AI models."""

    SAFETY_SETTINGS = [
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    def __init__(self):
        """Initialize the analyzer."""

    def read_reviews(self, reviews_list):
        """
        Read reviews from a list of dictionaries.

        Args:
            reviews_list (list):
                A list of dictionaries where each dictionary contains a 'review_text' key.

        Returns:
            str: A string containing all reviews, separated by " >>>".
        """
        if not reviews_list:
            raise ValueError("No reviews found in the provided list.")

        try:
            reviews = [
                element["review_text"]
                for element in reviews_list
                if "review_text" in element.keys()
            ]
            return " >>>".join(reviews)
        except Exception as e:
            raise ValueError(f"No reviews found in the provided list due to error {e}") from e

    def generate_summary(self, reviews, api_key1, safety="off"):
        """
        Generate a summary of reviews using an AI model.

        Args:
            reviews (str): The reviews to summarize.
            api_key1 (str): The API key for the AI model.
            safety (str, optional): Safety mode for content generation. Defaults to 'off'.

        Returns:
            str: The generated summary.
        """
        try:
            genai.configure(api_key=api_key1)
            model1 = genai.GenerativeModel("gemini-1.5-pro")

            prompt = f"""
                        You are summarizing Letterboxd reviews.  Given a collection of reviews, create a short, 
                        witty, and humorous paragraph that captures the overall sentiment and tone of the reviewers. 
                        Focus on the reviewers' reactions to the film itself, not just the plot.  
                        Write in a style that mimics the reviewers' own voices, but avoid overly conversational or informal language.
                        The goal is to give a potential viewer a sense of what it's like to experience the film based on the reviews - 
                        it should read like an actual Letterboxd reviewer is writing the review.
                        Avoid cheesy, overused language (avoid phrases like prepare to, rollercoaster etc.)- 
                        write in a manner similar to the reviews provided. Keep the summary *stricttly* under 200 words.
                        - Use only the reviews provided
                        - you cannot access real time information about the movies

                        Reviews:
                        {reviews}
                    """

            if safety == "off":
                prompt += "\n- Do not generate publicly offensive language."

            response = model1.generate_content(
                prompt, safety_settings=self.SAFETY_SETTINGS
            )
            if len(response.text.strip()) > 210:
                raise SummaryError("Summary over 210 words")
            return response.text

        except Exception as error:
            raise ValueError(f"Error generating summary: {error}") from error

    def generate_aspects(self, reviews, api_key2, safety="off"):
        """
        Generate aspect-based sentiment analysis of reviews using an AI model.

        Args:
            reviews (str): The reviews to analyze.
            api_key2 (str): The API key for the AI model.
            safety (str, optional): Safety mode for content generation. Defaults to 'off'.

        Returns:
            str: The generated aspect analysis.
        """
        try:
            genai.configure(api_key=api_key2)
            model2 = genai.GenerativeModel("gemini-1.5-pro")

            prompt = f"""
                        The following is a collection of movie reviews from Letterboxd. 
                        Each new review starts with ">>>".

                        Please analyze these reviews and identify the top 5 most mentioned cinematic aspects of the movie. 
                        For each aspect, provide the following:

                        1. The percentage of reviews that mention the aspect positively (as an integer).
                        2. The percentage of reviews that mention the aspect negatively (as an integer).

                        Please return the results as a Python dictionary string that can be directly evaluated using `ast.literal_eval()`. 
                        The dictionary should have:
                        - The cinematic aspect names (e.g., "Acting", "Direction", "Dialogue", "Color Scheme" etc.) as keys (strings).
                        - The values should be lists containing *exactly two integers*:
                            - The first integer represents the percentage of reviews mentioning the aspect positively.
                            - The second integer represents the percentage of reviews mentioning the aspect negatively.

                        While calculating the percentages, take into account ALL the reviews, not just the ones that mention that aspect.

                        Example output format:
                            {{
                                "Dialogue": [30, 10],
                                "Direction": [20, 15],
                                "Cinematography": [2, 10],
                                "Music": [5, 8],
                                "Plot": [3, 3],
                                "Actor Name": [2, 1],
                                "Director Name": [1, 2]
                            }}
                        Do not output the exact same dictionary as the
                        example output please. Aspects can include, but
                        are not limited to: acting, direction, cinematography,
                        sound/music, themes, pacing, performances, visuals, plot,
                        character development, etc. Do not shy away from
                        emphasising on negative aspects if that is the case.
                        The sum of positive and the negative review percentage will
                        likely be much less than 100, which is expected and okay.
                        Reviews:
                        {reviews}
                    """

            if safety == "off":
                prompt += "\n- Do not generate publicly offensive language."

            response = model2.generate_content(
                prompt, safety_settings=self.SAFETY_SETTINGS
            )
            return response.text

        except Exception as error:
            print(f"An error occurred: {error}")
            raise

    def aspect_processor(self, aspect_string):
        """
        Processes the aspect-based analysis string and returns a sorted list of aspects.

        Args:
            aspect_string (str): The aspect analysis string to process.

        Returns:
            list: A sorted list of aspects and their percentages.
        """
        try:
            match = re.search(r"\{([\s\S]*)\}", aspect_string)
            if match is None:
                raise AspectFormatError("Invalid aspect format")

            cleaned_string = "{" + match.group(1).strip() + "}"
            aspect_dict = ast.literal_eval(cleaned_string)
            assert isinstance(aspect_dict, dict)

            aspects = []
            for aspect, details in aspect_dict.items():
                if isinstance(details, list):
                    if (
                        len(details) == 2
                        and isinstance(details[0], int)
                        and isinstance(details[1], int)
                    ):
                        try:
                            positive_percentage = int(details[0])
                            negative_percentage = int(details[1])
                            total_mentions = positive_percentage + negative_percentage
                            aspects.append(
                                [
                                    total_mentions,
                                    aspect.title(),
                                    positive_percentage,
                                    negative_percentage,
                                ]
                            )

                        except ValueError as error:
                            print(f"Error converting percentages for {aspect}: {error}")
                            continue  # Skip to the next aspect

                    elif len(details) == 0:  # Handle empty lists gracefully
                        print(f"No details provided for {aspect}. Skipping.")
                        continue  # Skip to the next aspect
                    else:
                        print(f"Invalid format for aspect '{aspect}'. Skipping.")
                        continue  # Skip to the next aspect

                else:
                    print(f"Invalid format for aspect '{aspect}'. Skipping.")
                    continue  # Skip to the next aspect

            aspects.sort(reverse=True, key=lambda x: x[0])
            sorted_aspects = [aspect[1:] for aspect in aspects]  # Remove total mentions

            return sorted_aspects

        except (json.JSONDecodeError, AssertionError, ValueError) as error:
            print(error)
            raise  # Re-raise the exception

    def get_results(self, reviews, api_key1, api_key2, safety="off"):
        """
        Generates a summary and aspect analysis for the given movie reviews.

        Args:
            reviews (str): The movie reviews to analyze.
            api_key1 (list): A list of API keys for generating the summary.
            api_key2 (list): A list of API keys for generating aspect analysis.
            safety (str, optional): Safety mode for content generation. Defaults to 'off'.

        Returns:
            tuple: A tuple containing the generated summary (str) and the aspect list (list).
        """
        if len(reviews.strip()) < 400:
            raise ValueError("Not enough reviews found")
        summary = None
        for i in range(3):
            try:
                summary = self.generate_summary(reviews, api_key1[i], safety=safety)
                if len(summary.split()) > 210:
                    raise SummaryError("Summary too long")
                break
            except (SummaryError, ValueError, TypeError, KeyError) as error:
                print(f"Error generating summary: {error}")
                continue
        else:
            print("Failed to generate summary after 3 tries")
        aspect_list = None
        for i in range(3):
            try:
                aspects = self.generate_aspects(reviews, api_key2[i], safety=safety)
                aspect_list = self.aspect_processor(aspects)
                break
            except (AspectFormatError, ValueError, TypeError, KeyError) as e:
                print(f"Error generating summary: {e}")
                continue
        else:
            print("Failed to generate aspects after 3 tries")
            aspect_list = None

        return summary, aspect_list
