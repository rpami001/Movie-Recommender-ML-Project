#  import the libraries
import pandas as pd
import glob
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
from sklearn.model_selection import train_test_split
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.decomposition import TruncatedSVD

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
movies1 = pd.read_csv("combined_movies.csv")
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

svd_df = pd.DataFrame(data=X.toarray())

# Create a DataFrame with the reduced components
svd_df_1 = pd.DataFrame(data=X1.toarray())

print(svd_df_1)

# Concatenate DataFrames by columns
concatenated_df = pd.concat([svd_df, svd_df_1], axis=1)
print(concatenated_df)

# Apply KMeans clustering
num_clusters = 6  # Adjust the number of clusters as needed
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(concatenated_df)

# Assign cluster labels to reviews
concatenated_df['sentiment_cluster'] = kmeans.labels_
# Convert column names to strings 
concatenated_df.columns = concatenated_df.columns.astype(str)
print(concatenated_df)


from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Assuming concatenated_df is your DataFrame
# Drop the 'sentiment_cluster' column if it's already added
# features_df = concatenated_df.drop('sentiment_cluster', axis=1)

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(concatenated_df)

# Perform PCA
pca = PCA(n_components=400)  # Adjust the number of components as needed
principal_components = pca.fit_transform(scaled_data)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(data=principal_components)

# Apply KMeans clustering
num_clusters = 6  # Adjust the number of clusters as needed
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(pca_df)
# Optionally add the cluster labels back to the DataFrame
pca_df['sentiment_cluster'] = kmeans.labels_

print(pca_df)
# Combine the original data with concatenated_df
combined_df = pd.concat([df[['movie_name', 'rating', 'genre']], concatenated_df], axis=1)

print(combined_df)


# Evaluate the model 
#from sklearn.metrics import silhouette_score
#sillhouette_avg = silhouette_score(pca_df.drop('sentiment_cluster', axis=1), pca_df['sentiment_cluster'])
#print(f'Sillhouette Score: {sillhouette_avg}')

#X_pca = pca_df.drop('sentiment_cluster')
Y_pca = pca_df['sentiment_cluster']
X_pca = pca_df.drop(columns = 'sentiment_cluster')
# Split data into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X_pca, Y_pca, test_size=0.2, random_state=42)

# Train KMeans clustering model
num_clusters = 6
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X_train)

# Assign cluster labels to training data
#Y_train['sentiment_cluster'] = kmeans.labels_

# Predict cluster labels for the test set
test_labels = kmeans.predict(X_test)

ari_score = adjusted_rand_score(Y_test, test_labels)
print(ari_score)

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
    if user_mood == 'Excitement':
        recommended_movies = movies[(movies['sentiment_cluster'] == 1) | (movies['sentiment_cluster'] == 5)]
    elif user_mood == 'Sad':
        recommended_movies = movies[(movies['sentiment_cluster'] == 0)]
    elif user_mood == 'Feminine':
        recommended_movies = movies[(movies['sentiment_cluster'] == 4) | (movies['sentiment_cluster'] == 2)]
    elif user_mood == 'Passionate':
        recommended_movies = movies[(movies['sentiment_cluster'] == 2) | (movies['sentiment_cluster'] == 3) | (movies['sentiment_cluster'] == 5)]  
    elif user_mood == 'Happy':
        recommended_movies = movies[(movies['sentiment_cluster'] == 1) | (movies['sentiment_cluster'] == 0)]
    elif user_mood == 'Pure':
        recommended_movies = movies[(movies['sentiment_cluster'] == 3)]
    elif user_mood == 'Melancholic':
        recommended_movies = movies[(movies['sentiment_cluster'] == 0)]
    elif user_mood == 'Sanguine':
        recommended_movies = movies[(movies['sentiment_cluster'] == 4) | (movies['sentiment_cluster'] == 2)]
    elif user_mood == 'Choleric':
        recommended_movies = movies[(movies['sentiment_cluster'] == 2) | (movies['sentiment_cluster'] == 3) | (movies['sentiment_cluster'] == 5)]
    elif user_mood == 'Phlegmatic':
        recommended_movies = movies[(movies['sentiment_cluster'] == 1) | (movies['sentiment_cluster'] == 0)]
    else:  # neutral mood
        recommended_movies = movies[(movies['sentiment_cluster'] == 0)]

    # Sort the filtered movies by 'rating' (highest first) and then by 'year' (latest first)
    recommended_movies_sorted = recommended_movies.sort_values(by=['rating', 'year'], ascending=[False, False])
    
    result = recommended_movies_sorted[['movie_name', 'genre', 'year', 'rating', 'sentiment_cluster']].head(top_n)

    #print(f'M<MOD: {user_mood}')
    print(f'{result}')

    return result['movie_name'].tolist()
    # Get the top N movies based on the user's mood, highest rating, and latest year
    #return recommended_movies_sorted[['movie_name', 'genre', 'year', 'rating']].head(top_n)


# Recommend movies based on user's mood
#recommended_movies = recommend_movies_based_on_user_mood("positve", df, 5)
#recommended_movies_1 = recommend_movies_based_on_user_mood("melancholic", df, 5)
#recommended_movies_2 = recommend_movies_based_on_user_mood("sanguine", df, 5)
# print("Recommended Movies based on your mood:")
#print(f'TEST1: {recommended_movies}')
#print(f'TEST2: {recommended_movies_1}')
#print(f'TEST3: {recommended_movies_2}')