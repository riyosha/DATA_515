"""
API for scraping movie details and reviews from Letterboxd
"""
import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify
from src.helpers.scrapers import movie_details_scraper,scrape_reviews
from src.helpers.letterboxd_analyzers import LetterboxdReviewAnalyzer
from src.helpers.roast_generator import LetterboxdRoastAnalyzer
from src.helpers.scrapers_roast import scrape_user_reviews,scrape_user_stats

load_dotenv()
# Set up Google Gemini API key
GEMINI_API_KEY_RIO1 = os.getenv("GEMINI_API_KEY_RIO1")
GEMINI_API_KEY_RIO2 = os.getenv("GEMINI_API_KEY_RIO2")
GEMINI_API_KEY_RIO3 = os.getenv("GEMINI_API_KEY_RIO3")
GEMINI_API_KEY_SAI1 = os.getenv("GEMINI_API_KEY_SAI1")
GEMINI_API_KEY_SAI2 = os.getenv("GEMINI_API_KEY_SAI2")
GEMINI_API_KEY_SAI3 = os.getenv("GEMINI_API_KEY_SAI3")

GEMINI_API_KEY_RIO = [GEMINI_API_KEY_RIO1, GEMINI_API_KEY_RIO2, GEMINI_API_KEY_RIO3]
GEMINI_API_KEY_SAI = [GEMINI_API_KEY_SAI1, GEMINI_API_KEY_SAI2, GEMINI_API_KEY_SAI3]


analyze = LetterboxdReviewAnalyzer()
roaster = LetterboxdRoastAnalyzer()

app = Flask(__name__)

@app.route('/movie_details', methods=['POST'])
def scraping_movie_details():
    """Scrapes movie details from a Letterboxd movie page"""
    try:
        data = request.get_json()
        film_url = data.get('film_url')

        if not film_url:
            return jsonify({'error': 'film_url is required'}), 400

        movie_details = movie_details_scraper(film_url)
        reviews = scrape_reviews(film_url)
        reviews_text = analyze.read_reviews(reviews)
        summary, aspects = analyze.get_results(reviews_text,GEMINI_API_KEY_RIO,GEMINI_API_KEY_SAI)

        return jsonify({
            'movie_details': movie_details,
            'summary': summary,
            'aspects': aspects
        })

    except KeyError:
        return jsonify({'error': 'Invalid JSON format or missing key'}), 400
    except ValueError as ve:
        return jsonify({'error': f'Value error: {str(ve)}'}), 400
    except requests.exceptions.RequestException as re:
        return jsonify({'error': f'Request failed: {str(re)}'}), 500

@app.route('/roast', methods=['POST'])
def username_roast():
    """Roasts the user based on their Letterboxd profile"""
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({'error': 'username is required'}), 400

        user_reviews = scrape_user_reviews(username, n_pages=10)
        user_stats = scrape_user_stats(username)
        roast = roaster.get_results(user_reviews,user_stats,GEMINI_API_KEY_SAI)

        return jsonify({
            'roast': roast
        })

    except KeyError:
        return jsonify({'error': 'Invalid JSON format or missing key'}), 400
    except ValueError as ve:
        return jsonify({'error': f'Value error: {str(ve)}'}), 400
    except requests.exceptions.RequestException as re:
        return jsonify({'error': f'Request failed: {str(re)}'}), 500

if __name__ == '__main__':
    app.run()
