# Background

The problem being addressed is to help indivuiduals evaluate movies and help them decide what to watch more quickly. In addition we would like to provide a fun and entertaining analysis of viewers Letterboxd account.


# User Profiles

## User Profile 1

Name: Average Joe

Joe wants to pick a good movie for casual viewing while eating dinner.

Uses our summarizing tool to get a general summary of reviews and is able to recognize movie aspects they like such as: acting, direction, excellent cinematography, humor etc...

Needs to get a list of movies to be able to pick the right one that aligns with his interests

Doesn’t have relevant technical skills and values a simple user interface 

## User Profile 2

Name: Cinema Cindy

Cindy is going to the movies later in the evening and does not know what movie to pick. 

Cindy uses the tool to see the sentiment of all the available screenings at AMC to help her make a selection for what movie to watch.

Cindy needs help picking a movie, and has advanced web-surfing and TikTok skills.

## User Profile 3

Name: Edgineer the technician

Edgineer wants to scale the letterboxd sentiment model to potentially sell it to Letterboxd

Edgineer and co will: 
- Increase the database size by populating with more movies
- Add a feature to personally roast a Letterboxd user’s profile 
- Improve efficiency and time taken to present results

Edgineer needs more to evaluate LLM options and determine how to get more compute resources for the model.

Edgineer is a software developer and is learning how to deploy, maintain and scale SOTA deep learning, NLP and LLM models.

# Data Sources

## Data Source 1: Letterboxd Movie Reviews
https://www.kaggle.com/datasets/riyosha/letterboxd-worst-250-movie-reviews-87k
https://www.kaggle.com/datasets/riyosha/letterboxd-movie-reviews-90000

This dataset of movie reviews will help us provide quick analysis via our sentiment and aspect defining model.

## Data Source 2: User Letterboxd Account

We will instruct the user to export their Letterboxd account data and provide it to our application via our application. Every user letterboxd data will follow the same structure and consists of directories and subdirectories of CSV files. The files are organized around user actions such as reviews.csv, rating.csv, watched.csv

# Use Cases

## Use Case 1: Evaluate a movie Letterboxd movie URL

User: Selects Analyze button

System: Prompts user to provide a letterboxd movie URL

User: Provides Movie URL

System: 
- Display ‘fetching data’

- Scrape top 100 most popular reviews from the url into a .csv file

- Use ML model to generate an aspect based summary from the .csv file
	
- Display generated summary

User: Provides another Movie URL

Repeat
	   
## Use Case 2: Roast a User's Letterboxd Account

User: Selects Roast button

System: Prompts and instructs user how to provide letterboxd account data

User: Enter Letterboxd account data

System: Analyze and process user data based on provided .csv file

User: Wait for output

System: Use model to generate roast 
   
User: Laugh and share with friends

System: Profit
