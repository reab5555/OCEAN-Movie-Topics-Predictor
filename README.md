# OCEAN-Movie-Topics-Predictor

## Project Description
This project aims to analyze the relationship between movie keywords/topics and personality traits based on the Big Five personality model.   
   
The K-Nearest Neighbors (KNN) algorithm is used to predict which keywords or topics are associated with specific personality traits and gender by finding the most similar keywords in the dataset. For each trait and gender combination, KNN identifies the 25 nearest keywords based on cosine similarity, calculates their similarity scores, and generates word clouds to visualize these associations. 
   
## Dataset
The MyPersonality dataset derived from a Facebook app comprises personality scores of user's that liked certain movies, along with demographic and profile data from users who consented to share their information for research (Approximately 1000 users). The dataset we have contains a list of about 850 movie titles facebook user's liked and their aggregated average measures of the users in terms of each personality trait, including age and gender (currently, data per user is not available).
