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
            raise ValueError(
                f"No reviews found in the provided list due to error {e}"
            ) from e

    def read_user_data(self, reviews_list):
        """
        Reads reviews and statistics, and formats them into a single string.

        Args:
            reviews_list (list): A list of dictionaries, each containing a
                'review_text' key.
        Returns:
            str: A string that combines all reviews for prompt
                generation.

        Raises:
            ValueError: If reviews_list is empty.
        """
        if not reviews_list:
            raise ValueError("No reviews provided.")

        # Combine reviews by joining each review_text with a delimiter.
        reviews_text = " >>> ".join(
            element["movie_name"]
            + ", "
            + element["rating"]
            + ": "
            + element["review_text"]
            for element in reviews_list
            if "review_text" in element and "rating" in element and "movie_name" in element
            and element['review_text'] and element['rating'] and element['movie_name']
        )

        return reviews_text

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
            if len(response.text.split()) > 210:
                raise SummaryError("Summary over 200 words")
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
            raise ValueError(f"Error generating aspects: {error}") from error

    def aspect_processor(self, aspect_string):
        """
        Processes the aspect-based analysis string and returns a sorted list of aspects.

        Args:
            aspect_string (str): The aspect analysis string to process.

        Returns:
            list: A sorted list of aspects and their percentages.
        """
        try:
            # re pattern helps us extract content between curly brackets
            match = re.search(r"\{([\s\S]*)\}", aspect_string)
            if match is None:
                raise AspectFormatError("Invalid aspect format")

            cleaned_string = "{" + match.group(1).strip() + "}"
            aspect_dict = ast.literal_eval(cleaned_string)

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
                            aspects.append(
                                [
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

            aspects.sort(reverse=True, key=lambda x: x[1] + x[2])

            return aspects

        except (json.JSONDecodeError, AssertionError, ValueError) as error:
            print(error)
            raise

    def generate_taste_match(
        self, user_reviews, movie_reviews, movie_name, api_key3
    ):
        """
        Generate a taste match paragraph for a user and a given movie.

        Args:
            user_reviews (str): The user reviews to analyze.
            movie_reviews (str): The movie reviews to analyze.
            api_key3 (str): The API key for the AI model.
            safety (str, optional): Safety mode for content generation. Defaults to 'off'.

        Returns:
            str: The generated taste match analysis.
        """
        try:
            genai.configure(api_key=api_key3)
            model3 = genai.GenerativeModel("gemini-1.5-pro")

            prompt = f"""
                        The moview_reviews is a collection of movie reviews from Letterboxd. 
                        Each new review starts with ">>>".

                        The user_reviews is a collection of a Letterboxd user's movie reviews from Letterboxd. 
                        Each new review starts with ">>>", with this format "movie_name, rating: review_text".

                        Please analyze both these data and generate a paragraph about the taste match
                        of the user and the movie. 
                        
                        Check if the {movie_name} is present in the user reviews. If it is,
                        then DO NOT generate a taste match paragraph for this movie.
                        simply return the user's own review like this - 
                        'You've already reviewed this movie! You said - (user's own review text, without the movie name and rating)'
                        
                        Otherwise, depending on the aspects the user has liked/disliked 
                        the most in their own reviews, what might they like/dislike about this particular movie? 
                        Keep your response brief and *STRCITLY* under 200 words and don't give spoilers.
                        Address it to the user themself in 2nd person.

                        

                        movie_reviews:
                        {movie_reviews}
                        user_reviews:
                        {user_reviews}
                    """

            prompt += "\n- Do not generate publicly offensive language."

            response = model3.generate_content(
                prompt, safety_settings=self.SAFETY_SETTINGS
            )
            if len(response.text.split()) > 210:
                raise SummaryError("Summary over 200 words")

            return response.text

        except Exception as error:
            raise ValueError(f"Error generating taste match: {error}") from error

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
        if len(reviews.split()) < 400:
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

    def get_taste_match_result(
        self, user_reviews, movie_reviews, movie_name, api_key3
    ):
        """
        Generates a taste match summary between given movie reviews and user reviews.

        Args:
            movie_reviews (str): The movie reviews to analyze.
            user_reviews (str): The user reviews to analyze.
            api_key3 (list): A list of API keys for generating aspect analysis.
            safety (str, optional): Safety mode for content generation. Defaults to 'off'.

        Returns:
            string: a <= 200 word taste match summary.
        """
        if len(user_reviews.split()) < 100:
            raise ValueError("Not enough user reviews found")
        if len(movie_reviews.split()) < 400:
            raise ValueError("Not enough movie reviews found")

        taste_match = None
        for i in range(3):
            try:
                taste_match = self.generate_taste_match(
                    user_reviews, movie_reviews, movie_name, api_key3[i]
                )
                if len(taste_match.split()) > 210:
                    raise SummaryError("Taste match too long")
                break
            except (SummaryError, ValueError, TypeError, KeyError) as error:
                print(f"Error generating taste match: {error}")
                continue
        else:
            print("Failed to generate taste match after 3 tries")

        return taste_match
