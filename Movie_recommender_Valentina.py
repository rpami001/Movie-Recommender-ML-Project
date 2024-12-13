#  import the libraries
import pandas as pd
import glob
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
# cobine the movies into one dataset
# csv_files = glob.glob("Movies/*.csv")

# dfs = []
# for file in csv_files:
#     df = pd.read_csv(file)
#     dfs.append(df)
# all_movies = pd.concat(dfs)

# movies = all_movies.drop_duplicates(subset=['movie_name'], keep='first')
# movies.to_csv('combined_movies.csv', index=False)
# read csv file as dataframe
movies1 = pd.read_csv("C:\\Users\\vtebo\\Movie-Recommender-ML-Project\\combined_movies.csv")
#shuffle data so it is not biased
shuffled_data = movies1.sample(frac=1, random_state=42).reset_index(drop=True)
# Reduce data set to ease train
reduced_data = shuffled_data.sample(frac=0.50, random_state=42)
reduced_data.to_csv("combined_movies", index = False)
df = pd.read_csv('combined_movies')
#drop null title
df['movie_name'].dropna

# perform sentiment analyses on the description column of the movies
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
# nltk.download('wordnet')
def preprocess_text(text):
    text = text.lower()  # Lowercasing
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)  # Removing repeated words
    text = re.sub(r'[^a-z\s]', '', text)  # Removing non-alphabetic characters
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  # Lemmatization
    return " ".join(words)

df['description'] = df['description'].apply(preprocess_text)
df['genre'] = df ['genre'].apply(preprocess_text)
# print(df['description'])
# print(df['genre'])

#get key words
vectorizer =CountVectorizer(stop_words=stopwords.words('english'), max_features=1000)
X1 = vectorizer.fit_transform(df['genre'])
keywords = vectorizer.get_feature_names_out()
# print('Top keywords:', keywords)

from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=500)

# Convert cleaned reviews into a TF-IDF matrix
X = vectorizer.fit_transform(df['description'])

tfidf_keywords = vectorizer.get_feature_names_out()
# print('TF-IDF Keywords:', tfidf_keywords)

from scipy.sparse import hstack
X_combined = hstack([X, X1])

from sklearn.cluster import KMeans
import numpy as np


# Apply KMeans clustering to classify the movies based of emotions
num_clusters = 6  # Assume 6 clusters for positive, negative, and neutral
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X_combined)

# Assign cluster labels to reviews
df['sentiment_cluster'] = kmeans.labels_

# Now we perform exploratory data analysis, we begin by converting the year column to an integer
# Custom function to convert Roman numerals to integers
def roman_to_int(roman):
    roman_dict = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    result = 0
    prev_value = 0
    for char in reversed(roman):
        value = roman_dict[char]
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    return result
# Convert Roman numerals to integers using apply and the custom function
# Function to handle conversion with try-except
df['year'] = df['year'].fillna(2000)
def convert_year(value):
    try:
        # Try converting to integer directly
        return int(value)
    except ValueError:
        # If it fails, try converting Roman numeral to integer
        return roman_to_int(value)

# Apply the conversion function to the 'year' column
df['year'] = df['year'].apply(convert_year)

# fill null values in the rating column with the mean of the column
df['rating'] = df['rating'].fillna(np.mean(df['rating']))

# recommendation is performed by comparing the user's mood with the label of the movies then the movies are recommended first of all based on ratings, then year.
def recommend_movies_based_on_user_mood(user_mood, movies, top_n=5):
    # Filter movies based on the user's mood
    if user_mood == 'melancholic':
        recommended_movies = movies[movies['sentiment_cluster'] == 3]
    elif user_mood == 'sanguine':
        recommended_movies = movies[movies['sentiment_cluster'] == 2]
    else:  # neutral mood
        recommended_movies = movies[movies['sentiment_cluster'] == 1]
    
    # Sort the filtered movies by 'rating' (highest first) and then by 'year' (latest first)
    recommended_movies_sorted = recommended_movies.sort_values(by=['rating', 'year'], ascending=[False, False])
    
    # Get the top N movies based on the user's mood, highest rating, and latest year
    return recommended_movies_sorted[['movie_name', 'genre', 'year', 'rating']].head(top_n)

# Recommend movies based on user's mood
# recommended_movies = recommend_movies_based_on_user_mood("positve", df, 5)
# print("Recommended Movies based on your mood:")
# print(recommended_movies)