# OCEAN-Movie-Topics-Predictor

# Movie Keywords and Personality Traits Analysis

## Project Description

This project aims to analyze the relationship between movie keywords and personality traits based on the Big Five personality model. Utilizing a dataset derived from the MyPersonality dataset, which includes 850 movies, each movie is annotated with an aggregated mean score for the five personality traits: Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism. Additionally, the dataset includes a mean gender score, where a score of 1 indicates female and 0 indicates male.

## Dataset

The dataset consists of the following columns:
- **keywords**: A list of keywords associated with each movie.
- **ope**: Mean score for Openness.
- **con**: Mean score for Conscientiousness.
- **ext**: Mean score for Extraversion.
- **agr**: Mean score for Agreeableness.
- **neu**: Mean score for Neuroticism.
- **gender**: Mean gender score (1 for female, 0 for male).

## Project Workflow

1. **Data Preprocessing**:
   - Load the dataset and filter out rows with missing values in the `keywords` and `gender` columns.
   - Split the `keywords` column so that each keyword is treated independently.
   - Expand the dataset such that each keyword has its own row.

2. **Grouping and Aggregation**:
   - Group the data by keyword and compute the mean scores for each personality trait and gender.

3. **Standardization**:
   - Standardize the personality trait scores to have a mean of 0 and a standard deviation of 1.

4. **K-Nearest Neighbors (KNN) Analysis**:
   - Use the KNN algorithm with cosine similarity to find the nearest keywords for predefined high and low trait examples for both males and females.
   - Generate word clouds to visualize the most associated keywords for each trait and gender combination.

5. **Results**:
   - Generate and display word clouds for each trait and gender combination.
   - Save the associated keywords and their similarity scores in a CSV file.

## Visualization

The project includes the generation of word clouds to visually represent the keywords most associated with high and low levels of each personality trait for both males and females. The colors of the word clouds are gender-specific: 'Reds' for males and 'Blues' for females.

## Results

The results, including the associated keywords and their similarity scores for each trait and gender combination, are saved in a CSV file named `keywords_associated_with_traits.csv`.

## How to Run

To run the analysis, ensure you have the required libraries installed:

```bash
pip install pandas scikit-learn matplotlib wordcloud
