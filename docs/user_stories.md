# Exercise: User Stories 

User Story 1

Average Joe

Wants to pick a good movie for casual viewing while eating dinner

Uses our summarizing tool to get a general summary of reviews based on aspects like acting, direction, cinematography, humor etc etc 

Needs to get a list of movies to be able to pick the right one that aligns with his interests

Doesn’t have relevant technical skills and values a simple user interface 

User Story 2

Cinema Cindy

Cindy is going to the movies later in the evening and does not know what movie to pick. 

Cindy uses the tool to see the sentiment of all the available options to help her make a selection for what movie to watch.

Cindy needs help picking a movie, and has advanced web-surfing skills.

User Story 3

Edgineer the technician

Edgineer wants to scale the model to potentially sell it to Letterboxd in the future

Edgineer and co will - 
Increase the database size 
Add a feature to personally roast a Letterboxd user’s profile 
Improve efficiency and time taken to present results

Edgineer needs more compute units(?)

Edgineer is learning how to deploy, maintain and scale SOTA deep learning, NLP and LLM models

# Exercise: Use Cases

User: Enter Letterboxd movie URL

System: Display ‘fetching data’
	   
   Scrape top 100 most popular reviews from the url into a .csv file

	  Use ML model to generate an aspect based summary from the .csv file
	
	  Display generated summary
	   

User: Enter Letterboxd user profile’s url

System: Fetch data from user’s letterboxd account into a .csv file

User: Wait for output

System: Use model to generate roast 
   
   Output roast



