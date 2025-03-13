"""
API for scraping movie details and reviews from Letterboxd
"""
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from helpers.scrapers import movie_details_scraper,scrape_reviews
from helpers.letterboxd_analyzers import LetterboxdReviewAnalyzer


load_dotenv()
# Set up Google Gemini API key
'''    api_keys_rio = os.getenv("GEMINI_API_KEY_RIO", "").split(",")
    api_keys_sai = os.getenv("GEMINI_API_KEY_SAI", "").split(",")
    for i in range(3): '''
api_key1 = os.getenv("GEMINI_API_KEY_RIO2")
api_key2 = os.getenv("GEMINI_API_KEY_SAI2")

analyze = LetterboxdReviewAnalyzer()

app = Flask(__name__)

@app.route('/')
def home():
    """Home route"""
    return "Letterboxd Review Analyzer is running!"

@app.route('/movie_details', methods=['POST'])
def movie_details():
    """Scrapes movie details from a Letterboxd movie page"""
    try:
        data = request.get_json()
        film_url = data.get('film_url')

        if not film_url:
            return jsonify({'error': 'film_url is required'}), 400
        movie_details = movie_details_scraper(film_url)

        return jsonify({
            'movie_details': movie_details,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/reviews', methods=['POST'])
def reviews():
    """Scrapes reviews from a Letterboxd movie page"""
    try:
        data = request.get_json()
        film_url = data.get('film_url')

        if not film_url:
            return jsonify({'error': 'film_url is required'}), 400
        reviews = scrape_reviews(film_url)
        reviews_text = analyze.read_reviews(reviews)
        summary, aspects = analyze.get_results(reviews_text,api_key1,api_key2)


        return jsonify({
            'summary': summary,
            'aspects': aspects
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()