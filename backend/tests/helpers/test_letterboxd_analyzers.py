"""Testing suite for the class LetterboxdAnalyzer"""

import unittest
from unittest.mock import patch
from src.helpers.letterboxd_analyzers import (
    LetterboxdReviewAnalyzer,
    AspectFormatError,
    SummaryError,
)  # Replace with actual module name


class TestLetterboxdReviewAnalyzer(unittest.TestCase):
    """Unit tests for the LetterboxdReviewAnalyzer class."""

    def setUp(self):
        """Set up the test environment and mock data."""
        self.analyzer = LetterboxdReviewAnalyzer()
        self.sample_reviews = [
            {
                "review_text": "Amazing cinematography and a gripping story!",
                "rating": "5",
            },
            {
                "review_text": "The acting was top-notch, but the plot felt weak.",
                "rating": "4",
            },
            {
                "review_text": "Loved the visuals, but the direction was a bit off.",
                "rating": "3",
            },
        ]
        self.mock_summary = (
            "A visually stunning movie with strong acting but a weak plot."
        )
        self.mock_aspects = """```python
                                {
                                    "Cinematography": [80, 20],
                                    "Acting": [70, 30],
                                    "Direction": [50, 50],
                                    "Humor/Comedy": [37, 15],
                                    "Visuals/Cinematography": [23, 2]
                                }
                                ```"""
        self.api_key1 = ["1", "2", "3"]
        self.api_key2 = ["4", "5", "6"]

    def test_read_reviews_success(self):
        """Test the read_reviews with valid input"""
        expected_output = (
            "Amazing cinematography and a gripping story! "
            ">>>The acting was top-notch, but the plot felt weak. "
            ">>>Loved the visuals, but the direction was a bit off."
        )
        self.assertEqual(
            self.analyzer.read_reviews(self.sample_reviews), expected_output
        )

    def test_read_reviews_empty_string(self):
        """Test the read_reviews method with empty string"""

        with self.assertRaisesRegex(
            ValueError, "No reviews found in the provided list."
        ):
            self.analyzer.read_reviews("")

    def test_read_reviews_half_valid(self):
        """Test the read_reviews method - half valid"""
        reviews_list = [
            {"review_text": "Amazing cinematography and a gripping story!"},
            {"rating": "4"},
            {"review_text": "Loved the visuals, but the direction was a bit off."},
        ]
        expected_output = (
            "Amazing cinematography and a gripping story! "
            ">>>Loved the visuals, but the direction was a bit off."
        )
        self.assertEqual(self.analyzer.read_reviews(reviews_list), expected_output)

    def test_aspect_processor_valid(self):
        """Test aspect_processor with valid aspect string."""
        processed_aspects = self.analyzer.aspect_processor(self.mock_aspects)
        expected_output = [
            ["Cinematography", 80, 20],
            ["Acting", 70, 30],
            ["Direction", 50, 50],
            ["Humor/Comedy", 37, 15],
            ["Visuals/Cinematography", 23, 2],
        ]
        self.assertEqual(processed_aspects, expected_output)

    def test_aspect_processor_half_valid(self):
        """Test aspect_processor with half complete aspect string."""
        aspects = """```python
                    {
                        "Cinematography": [80, 20],
                        "Acting": [70],
                        "Direction": {'pos': 50, 'neg': 50},
                        "Humor/Comedy": [37, 15],
                        "Visuals/Cinematography": 'veiwers loved it'
                    }
                    ```"""
        processed_aspects = self.analyzer.aspect_processor(aspects)
        expected_output = [["Cinematography", 80, 20], ["Humor/Comedy", 37, 15]]
        self.assertEqual(processed_aspects, expected_output)

    def test_aspect_processor_invalid(self):
        """Test aspect_processor with invalid aspect string."""
        with self.assertRaises(AspectFormatError):
            self.analyzer.aspect_processor("invalid string")

    def test_get_results_not_enough_reviews(self):
        """Test get_results with not enough reviews"""
        with self.assertRaisesRegex(ValueError, "Not enough reviews found"):
            self.analyzer.get_results(
                self.analyzer.read_reviews(self.sample_reviews),
                self.api_key1,
                self.api_key2,
            )

    @patch(
        "src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.generate_aspects"
    )
    @patch(
        "src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.generate_summary"
    )
    def test_get_results_success(self, mock_generate_summary, mock_generate_aspects):
        """Test get_results with enough reviews"""
        # Create test reviews
        reviews = [{"review_text": f"Review {i}"} for i in range(400)]
        review_text = self.analyzer.read_reviews(reviews)

        # Set up mock returns
        summary_text = (
            "Nolan's *Inception*: a heist movie, a sci-fi epic, "
            "a Cillian Murphy thirst trap. "
            "Is it gay to infiltrate your bro's subconscious? "
            "The internet seems to think so. JGL and Tom Hardy? "
            "Gay. Arthur and Eames? Gay. Ariadne? Gay icon. "
            "Even DiCaprio and Murphy? Suspiciously close. "
            "Forget the spinning top, the real question is: *who isn't* in "
            "love with Cillian Murphy? The plot? Convoluted, explained ad "
            "nauseam by Leo, yet somehow still a banger. BWAAAAHHHH, indeed. "
            "Just try to finish the film without a Wikipedia deep dive and a "
            "sudden urge to write Arthur/Eames fanfiction. It's a masterpiece, "
            "but don't trust anyone who claims to fully understand it on the first "
            "watch. (They're lying.) Prepare for horny confusion, existential dread, "
            "and the unshakeable feeling that Christopher Nolan is living in "
            "your head rent-free."
        )

        aspects_raw = """```python{
                        "Cinematography": [80, 20],
                        "Acting": [70, 30],
                        "Direction": [50, 50],
                        "Humor/Comedy": [37, 15],
                        "Visuals/Cinematography": [23, 2]
                    }```"""

        mock_generate_summary.return_value = summary_text
        mock_generate_aspects.return_value = aspects_raw

        result = self.analyzer.get_results(review_text, self.api_key1, self.api_key2)

        expected_aspects = [
            ["Cinematography", 80, 20],
            ["Acting", 70, 30],
            ["Direction", 50, 50],
            ["Humor/Comedy", 37, 15],
            ["Visuals/Cinematography", 23, 2],
        ]

        expected_result = (summary_text, expected_aspects)
        self.assertEqual(result, expected_result)

    @patch(
        "src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.generate_aspects"
    )
    @patch(
        "src.helpers.letterboxd_analyzers.LetterboxdReviewAnalyzer.generate_summary"
    )
    def test_get_results_all_attempts_fail(
        self, mock_generate_summary, mock_generate_aspects
    ):
        """Test get_results when all attempts to generate summaries and aspects fail."""

        reviews = [{"review_text": f"Review {i}"} for i in range(400)]
        review_text = self.analyzer.read_reviews(reviews)

        mock_generate_summary.side_effect = [
            SummaryError("Summary too long"),
            ValueError("Error in model response"),
            SummaryError("Invalid format"),
        ]

        mock_generate_aspects.side_effect = [
            AspectFormatError("Invalid aspect format"),
            ValueError("Model response error"),
            AspectFormatError("Parsing error"),
        ]

        result = self.analyzer.get_results(review_text, self.api_key1, self.api_key2)

        expected_result = (None, None)

        self.assertEqual(result, expected_result)

        self.assertEqual(mock_generate_summary.call_count, 3)
        self.assertEqual(mock_generate_aspects.call_count, 3)


if __name__ == "__main__":
    unittest.main()
