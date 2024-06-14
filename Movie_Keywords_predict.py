import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load the dataset
file_path = 'movies_big_five.csv'
data = pd.read_csv(file_path)

# Filter out NaNs and non-string keyword entries
data = data.dropna(subset=['keywords', 'gender'])
data = data[data['keywords'].apply(lambda x: isinstance(x, str) and x.strip() != '')]

# Extract keywords and treat each keyword independently
data['keywords'] = data['keywords'].apply(lambda x: x.split(','))

# Expand the data so that each keyword has its own row
expanded_data = data.explode('keywords')

# Filter out rows where keywords might be empty after exploding
expanded_data = expanded_data[expanded_data['keywords'].apply(lambda x: isinstance(x, str) and x.strip() != '')]

# Group by keyword and aggregate personality traits
grouped_keywords = expanded_data.groupby('keywords').agg({
    'ope': 'mean', 'con': 'mean', 'ext': 'mean', 'agr': 'mean', 'neu': 'mean', 'gender': 'mean'
}).reset_index()

# Standardize personality traits
scaler = StandardScaler()
traits = grouped_keywords[['ope', 'con', 'ext', 'agr', 'neu']]
traits_scaled = scaler.fit_transform(traits)
grouped_keywords[['ope', 'con', 'ext', 'agr', 'neu']] = traits_scaled

# Define the classes for high and low traits for male (0) and female (1)
input_traits_examples = {
    "High Openness Male": [1, 0, 0, 0, 0, 0],
    "Low Openness Male": [-1, 0, 0, 0, 0, 0],
    "High Conscientiousness Male": [0, 1, 0, 0, 0, 0],
    "Low Conscientiousness Male": [0, -1, 0, 0, 0, 0],
    "High Extraversion Male": [0, 0, 1, 0, 0, 0],
    "Low Extraversion Male": [0, 0, -1, 0, 0, 0],
    "High Agreeableness Male": [0, 0, 0, 1, 0, 0],
    "Low Agreeableness Male": [0, 0, 0, -1, 0, 0],
    "High Neuroticism Male": [0, 0, 0, 0, 1, 0],
    "Low Neuroticism Male": [0, 0, 0, 0, -1, 0],
    "High Openness Female": [1, 0, 0, 0, 0, 1],
    "Low Openness Female": [-1, 0, 0, 0, 0, 1],
    "High Conscientiousness Female": [0, 1, 0, 0, 0, 1],
    "Low Conscientiousness Female": [0, -1, 0, 0, 0, 1],
    "High Extraversion Female": [0, 0, 1, 0, 0, 1],
    "Low Extraversion Female": [0, 0, -1, 0, 0, 1],
    "High Agreeableness Female": [0, 0, 0, 1, 0, 1],
    "Low Agreeableness Female": [0, 0, 0, -1, 0, 1],
    "High Neuroticism Female": [0, 0, 0, 0, 1, 1],
    "Low Neuroticism Female": [0, 0, 0, 0, -1, 1]
}

# Define the traits to be analyzed
traits_to_analyze = ['ope', 'con', 'ext', 'agr', 'neu']
trait_names = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

# Fit KNN with cosine similarity
knn = NearestNeighbors(metric='cosine', n_neighbors=25)
knn.fit(np.hstack([traits_scaled, grouped_keywords[['gender']]]))

# Function to create word clouds
def create_wordcloud(word_freq, title, wordcloud_colors):
    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          colormap=wordcloud_colors).generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=15)
    plt.axis('off')
    plt.show()

# Generate word clouds for each trait and high/low combination
results = []
for description, traits in input_traits_examples.items():
    trait_name = next((name for name in trait_names if name.lower() in description.lower()), None)
    if not trait_name:
        continue

    gender = traits[-1]
    gender_label = "Male" if gender == 0 else "Female"
    trait_level = "High" if any(trait == 1 for trait in traits[:-1]) else "Low"

    input_traits_scaled = scaler.transform([traits[:-1]])
    input_traits_combined = np.hstack([input_traits_scaled, np.array([[gender]])])
    distances, indices = knn.kneighbors(input_traits_combined)

    associated_keywords = grouped_keywords.iloc[indices[0]]

    word_freq = {}
    for i in range(len(indices[0])):
        keyword = associated_keywords.iloc[i]['keywords']
        similarity = 1 - distances[0][i]  # Convert distance to similarity
        word_freq[keyword] = similarity

    # Set color based on gender
    wordcloud_colors = 'Reds' if gender == 0 else 'Blues'
    title = f"{trait_name} - {trait_level} - {gender_label}"

    create_wordcloud(word_freq, title, wordcloud_colors)

    # Save results
    result = {
        'Description': description,
        'Keyword': keyword,
        'Similarity': similarity,
        'Gender': gender_label,
        'Trait_Level': trait_level,
        'Trait_Name': trait_name
    }
    results.extend([{'Description': description, 'Keyword': k, 'Similarity': s, 'Gender': gender_label, 'Trait_Level': trait_level, 'Trait_Name': trait_name} for k, s in word_freq.items()])

    # Print results
    print(f"Description: {description}")
    print("Associated Keywords and Similarities:")
    for keyword, similarity in word_freq.items():
        print(f"{keyword}: {similarity:.2f}")
    print("\n")

# Save results as a dataframe to a CSV file
results_df = pd.DataFrame(results)
results_df.to_csv('keywords_associated_with_traits.csv', index=False)
