"""
API for scraping movie details and reviews from Letterboxd
"""

from flask import Flask, request, jsonify
from helpers.scrapers import movie_details_scraper,scrape_reviews

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

        return jsonify({
            'reviews': reviews,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()