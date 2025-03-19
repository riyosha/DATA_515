# Letterboxd Movie Analysis & Roast Tool - Functional Specification

## Overview
This project is an interactive web tool that helps users analyze movies and decide what to watch by summarizing Letterboxd reviews. Additionally, it provides an entertaining and witty roast of a user’s Letterboxd profile based on their viewing habits and ratings.

## User Profiles
### User Profile 1: Average Joe
- **Goal:** Wants to pick a good movie for casual viewing while eating dinner.
- **Behavior:** Uses the summarizing tool to get a general review summary and identify movie aspects they like (acting, direction, cinematography, humor, etc.).
- **Needs:** A simple, user-friendly interface that provides a list of movies aligned with their interests.
- **Technical Skill Level:** Low; values ease of use.

### User Profile 2: Cinema Cindy
- **Goal:** Needs help picking a movie to watch in the evening.
- **Behavior:** Uses the tool to check the sentiment of available screenings at AMC before making a decision.
- **Needs:** A quick way to compare movie reception.
- **Technical Skill Level:** Advanced; comfortable with web navigation and social media platforms.

### User Profile 3: Edgineer the Technician
- **Goal:** Wants to scale the Letterboxd sentiment model to potentially sell it to Letterboxd.
- **Behavior:** Focuses on increasing the dataset size, improving efficiency, and adding a feature to roast a user’s profile.
- **Needs:** Insights on evaluating LLM options and compute resources for scaling the model.
- **Technical Skill Level:** High; software developer learning to deploy, maintain, and scale state-of-the-art NLP and LLM models.

## Core Features
- **Live-Scraped Movie Summaries** – Users enter a Letterboxd movie URL, and the system scrapes reviews in real-time to generate a concise summary and aspect-based sentiment analysis.
- **Live-Scraped User Profile Roasts** – Users enter their Letterboxd username, and the system scrapes their watch history, ratings, and habits to generate a detailed roast.
- **No Manual Data Uploads** – All data is live-scraped, ensuring accuracy and up-to-date insights.
- **LLM-Powered Analysis** – AI models process reviews to extract key themes, such as acting, cinematography, and plot, and generate an analytical summary.

## 1. Live Scraped Movie Details & Reviews
### How it Works
When a user enters a Letterboxd movie URL, the system scrapes the latest reviews and movie details in real-time.

### Scraped Data Fields
**Movie Information** (from `letterboxd.com/film/{movie-name}/`)
- **movie_name** – The name of the movie
- **year** – The movie’s release year
- **director** – The movie’s director
- **genres** – Genre(s) of the movie
- **synopsis** – The official movie synopsis
- **backdrop_image_url** – The background image URL for the movie

**Reviews** (from `letterboxd.com/film/{movie-name}/reviews/`)
- **rating** – The rating given by a user (if available)
- **review_text** – The content of the user’s review

### How the Data is Used
- Movie details are displayed in the UI for reference.
- Reviews are processed through an AI-powered aspect-based sentiment analysis model, identifying themes such as acting, cinematography, storytelling, and music.
- A summary is generated based on the most commonly expressed sentiments in the reviews.
- Users receive an informative snapshot of what people think about the movie.

## 2. Live Scraped User Letterboxd Data (For Roast Feature)
### How it Works
When a user enters their Letterboxd username, the system scrapes their profile details in real-time and generates a personalized roast based on their viewing habits.

### Scraped User Data Fields
**Reviews** (from `letterboxd.com/{username}/films/reviews/`)
- **movie_name** – The name of the reviewed movie
- **movie_url** – The Letterboxd link to the movie
- **rating** – The user's rating (if available)
- **watched_date** – The date the user watched the movie
- **review_text** – The content of the review

**Profile Statistics** (from `letterboxd.com/{username}/stats/`)
- **Total movies watched** – The total number of movies watched by the user
- **Total hours watched** – The cumulative hours of movies watched
- **Most-watched genre** – The genre the user watches the most
- **Most-watched actor** – The actor the user watches the most
- **Most-watched director** – The director the user watches the most
- **Longest streak (days)** – The longest consecutive days of movie-watching
- **Days with 2+ films watched** – The number of days where the user watched more than one movie

### How the Data is Used
- The roast generator analyzes trends in rating behavior, genre preferences, and watching patterns.
- The system detects patterns such as over-reliance on specific genres or consistently giving high ratings to low-rated movies.
- A roast is generated using LLM-based text generation, mimicking an in-depth Letterboxd film critique.

## Use Cases

### Use Case 1: Evaluate a Movie's Letterboxd Reviews (Live Scraping)
#### Steps
1. **User Action:** Clicks "Analyze" and enters a Letterboxd movie URL.
2. **System Action:**
   - Scrapes movie details, including title, director, year, genres, synopsis, and image.
   - Scrapes the latest reviews for the movie.
   - Processes reviews through LLM-powered sentiment and aspect analysis.
   - Displays:
     - Movie information
     - A generated review summary
     - Aspect-based analysis (e.g., acting, cinematography, plot, music, etc.)

### Use Case 2: Roast a User's Letterboxd Account (Live Scraping)
#### Steps
1. **User Action:** Clicks "Roast" and enters their Letterboxd username.
2. **System Action:**
   - Scrapes live data from the user’s Letterboxd profile, including:
     - All reviews
     - Movie ratings and patterns
     - Most-watched actors, directors, and genres
     - Movie-watching streaks and habits
   - Generates a roast by analyzing:
     - Unusual rating decisions (e.g., 5 stars to widely disliked movies)
     - Over-reliance on specific actors, directors, or genres
     - Unusual binge habits (e.g., rewatching a single film excessively)
     - Review style patterns (lengthy essays vs. short reviews)
   - Outputs a roast paragraph that critiques the user’s movie-watching habits.

## Why This Approach
- **No manual data uploads** – Users only need to enter a movie URL or username.
- **Always up-to-date** – The system scrapes the latest data live, ensuring accuracy.
- **Fast and detailed** – Users receive instant insights into movies and their own viewing patterns.
- **AI-powered analysis** – Reviews are summarized into an easy-to-read and informative format.

## Conclusion
This project integrates live web scraping, AI-powered sentiment analysis, and a structured critique approach to provide a unique and engaging tool for movie enthusiasts. The system ensures that the data is always current, offering precise and insightful summaries and roasts based on real-time information.
