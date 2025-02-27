from IPython import get_ipython
from IPython.display import display
# %%
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import csv
import ast
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import google.generativeai as genai
import os
from matplotlib.patches import Rectangle
import io
import base64

app = Flask(__name__)


class LetterboxdReviewAnalyzer:
    def __init__(self):
      self.safety_settings = [
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
      ]

    def read_reviews(self, filename):
        try:
            reviews = []
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    reviews.append(row['Review Text'])

            if not reviews:
                print(f"No reviews found in {filename}")
                return None

            return "\n >>>".join(reviews)

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def generate_summary(self, reviews, api_key1):
        try:

          genai.configure(api_key=api_key1)
          model1 = genai.GenerativeModel("gemini-1.5-pro")

          prompt = f"""
          You are summarizing Letterboxd reviews.  Given a collection of reviews, create a short, witty, and humorous paragraph that captures the overall sentiment and tone of the reviewers.
          Focus on the reviewers' reactions to the film itself, not just the plot.  Write in a style that mimics the reviewers' own voices, but avoid overly conversational or informal language.
          The goal is to give a potential viewer a sense of what it's like to experience the film based on the reviews - it should read like an actual Letterboxd reviewer is writing the review.
          Avoid cheesy, overused language (avoid phrases like prepare to, rollercoaster etc.)- write in a manner similar to the reviews provided. Keep the summary *stricttly* under 200 words.
          - Use only the reviews provided
          - you cannot access real time information about the movies

          Reviews:
          {reviews}
          """

          response = model1.generate_content(
              prompt,
              safety_settings=self.safety_settings
          )

          return(response.text)

        except Exception as e:
            print(f"An error occurred: {e}")
            raise



    def generate_aspects(self, reviews, api_key2):
        try:
          genai.configure(api_key=api_key2)
          model2 = genai.GenerativeModel("gemini-1.5-pro")


          prompt = f"""
          The following is a collection of movie reviews from Letterboxd. Each new review starts with ">>>".

          Please analyze these reviews and identify the top 5 most mentioned cinematic aspects of the movie. For each aspect, provide the following:

          1. The percentage of reviews that mention the aspect positively (as an integer).
          2. The percentage of reviews that mention the aspect negatively (as an integer).

          Please return the results as a Python dictionary string that can be directly evaluated using `ast.literal_eval()`. The dictionary should have:
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
          Do not output the exact same dictionary as the example output please.
          Aspects can include, but are not limited to: acting, direction, cinematography, sound/music, themes, pacing, performances, visuals, plot, character development, etc.
          Do not shy away from emphasising on negative aspects if that is the case. The sum of positive and the negative review percentage will likely be much less than 100, which is expected and okay.
          Reviews:
          {reviews}
          """

          response = model2.generate_content(
            prompt,
            safety_settings=self.safety_settings
          )

          return(response.text)

        except Exception as e:
          print(f"An error occurred: {e}")
          raise



    def aspect_processor(self, aspect_string):
        try:
            aspect_dict = ast.literal_eval(aspect_string.lstrip('python').rstrip(''))
            assert isinstance(aspect_dict, dict)

            aspects = []
            for aspect, details in aspect_dict.items():
                if isinstance(details, list):
                    if len(details) == 2 and isinstance(details[0], int) and isinstance(details[1], int):
                        try:
                            positive_percentage = int(details[0])
                            negative_percentage = int(details[1])
                            total_mentions = positive_percentage + negative_percentage
                            aspects.append([total_mentions, aspect.title(), positive_percentage, negative_percentage])

                        except ValueError as e:
                            print(f"Error converting percentages for {aspect}: {e}")
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

        except (json.JSONDecodeError, AssertionError, ValueError) as e:
            raise  # Re-raise the exception


    def aspect_charts(self, aspect_list):

        aspects = [asp[0] for asp in aspect_list]
        positive = [asp[1] for asp in aspect_list]
        negative = [asp[2] for asp in aspect_list]

        text_color = "#E0E0E0"

        x = np.arange(len(aspects))  # Label locations
        width = 0.4  # Bar width

        # Set Seaborn style
        sns.set_style("darkgrid")

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#181818")  # Set entire figure background
        ax.set_facecolor("#181818")

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Create bars
        rects1 = ax.bar(x - width/2, positive, width, label='Positive', color="#2ECC71", edgecolor="#2ECC71")
        rects2 = ax.bar(x + width/2, negative, width, label='Negative', color="#E67E22", edgecolor="#E67E22")


        # Labels, title, and legend
        ax.set_xlabel('Movie Aspects', fontsize=15, fontweight='bold', color=text_color)
        ax.set_ylabel('Percentage of Reviewers', fontsize=15, fontweight='bold', color=text_color)

        ax.set_title('Reviewers Say...', fontsize=20, fontweight='bold', color=text_color, pad=30)
        ax.set_xticks(x)
        ax.set_ylim(0,100)
        ax.set_xticklabels([f"{a}" for a in aspects], rotation=30, ha="right", fontsize=12, color=text_color)
        ax.legend(fontsize=12, frameon=True, loc='upper right')

        ax.yaxis.label.set_color(text_color)
        ax.tick_params(axis='y', labelcolor=text_color)  # Set y-axis ticks to light grey
        ax.tick_params(axis='x', labelcolor=text_color)

        # remove gridlines
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)

        # Display values on bars
        def add_labels(rects, color):
            for rect in rects:
                height = rect.get_height()
                if height > 0:  # Only annotate if the value is greater than 0
                    ax.annotate(f'{height}%',
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 5),  # Offset above the bar
                                textcoords="offset points",
                                ha='center', fontsize=12, fontweight='bold', color=color)

        add_labels(rects1, "#228B22")  # Greenish
        add_labels(rects2, "#B22222")  # Reddish

        # Adjust layout
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", transparent=True, bbox_inches="tight")
        buffer.seek(0)
        plt.close()

        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode("utf-8")
        return graphic


    def get_results(self, reviews, movie_name, api_key1, api_key2):


      for i in range(3):
        try:
          summary = self.generate_summary(reviews,api_key1[i])
          with open(f'{movie_name}_summary.txt', 'w', encoding='utf-8') as f:  # 'w' mode for writing (overwrites existing file)
            f.write(summary)
          print(f"String saved to {movie_name}_summary.txt")
          break  # Exit loop if successful
        except Exception as e:
          print(f"Error saving string to file: {e}")
      else:
        print("Failed to save summary to file after 3 attempts.")
        return None

      for i in range(3):
            try:
                aspects = self.generate_aspects(reviews,api_key2[i])
                aspect_list = self.aspect_processor(aspects)
                chart = self.aspect_charts(aspect_list[:5])
                break  # Exit loop if successful
            except Exception as e:
                print(f"Error processing aspects: {e}. Retrying...")
      else:
          print("Failed to process aspects after 3 attempts.")
          return None

      return summary, aspect_list, chart



def scrape_reviews(film_url):
    def fetch_reviews(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve reviews from {url}. Status code: {response.status_code}")
            return None
    movie_name = film_url.split('/')[-2]
    with open(f'{movie_name}_reviews.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Rating', 'Review Text'])

        for page in range(1, 31):
            reviews_url = f"{film_url}reviews/by/activity/page/{page}/"
            html_content = fetch_reviews(reviews_url)

            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                reviews_section = soup.find('section', class_='viewings-list')

                if reviews_section:
                    reviews = reviews_section.find_all('li', class_='film-detail')

                    for review in reviews:
                        review_body = review.find('div', class_='js-review-body')
                        if review_body:
                            review_text = review_body.find('p').get_text(strip=True) if review_body.find('p') else ''

                            rating_span = review.find('span', class_='rating')
                            rating = rating_span.get_text(strip=True) if rating_span else 'No Rating'

                            csv_writer.writerow([rating, review_text])
                else:
                    print(f"No reviews section found on page {page}.")
            else:
                print(f"No reviews found or unable to fetch reviews from page {page}.")

    print(f"Reviews have been saved to {movie_name}_reviews.csv.")
    return movie_name

analyzer = LetterboxdReviewAnalyzer()

# API Endpoints

@app.route('/analyze', methods=['POST'])
def analyze_movie():
    try:
        data = request.get_json()
        film_url = data.get('film_url')

        if not film_url:
            return jsonify({'error': 'film_url is required'}), 400
        movie_name = scrape_reviews(film_url)
        reviews = analyzer.read_reviews(f'{movie_name}_reviews.csv')
        results = analyzer.get_results(reviews, movie_name, GEMINI_API_KEY_RIO, GEMINI_API_KEY_SAI)
        summary, aspect_list, chart = results

        return jsonify({
            'movie_name': movie_name,
            'summary': summary,
            'aspects': aspect_list,
            'chart' : chart
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        #clean up files
        os.remove(f'{movie_name}_reviews.csv')
        os.remove(f'{movie_name}_summary.txt')


if __name__ == '__main__':
    app.run(debug=True)
