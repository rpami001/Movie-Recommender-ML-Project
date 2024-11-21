import pandas as pd
from textblob import TextBlob

#Loading Dataset
movie_dataset = pd.read_csv('combined_movies.txt', delimiter = ',')

#Sentiment Analyzer
def sentiment_analysis(text):
    return TextBlob(text).sentiment.polarity

#Categorizing sentiment
def categorize_sentiment(score):
    if score > 0.2:
        return 'positive'
    
    elif score < -0.2:
        return 'negative'
    
    else:
        return 'neutral'

# Temperament keywords mapping
temperament_map = {
    'melancholic': {
        'keywords': ['sad', 'lonely', 'depressed', 'dark', 'bleak'],
        'target_sentiments': ['negative', 'neutral']
    },
    'sanguine': {
        'keywords': ['happy', 'joy', 'love', 'excited', 'positive'],
        'target_sentiments': ['positive']
    },
    'choleric': {
        'keywords': ['angry', 'rage', 'furious', 'hate', 'frustrated'],
        'target_sentiments': ['positive', 'neutral']
    },
    'phlegmatic': {
        'keywords': ['calm', 'peaceful', 'relaxed', 'content', 'quiet'],
        'target_sentiments': ['neutral', 'positive']
    }
}


# Function to check for keywords in description
def match_keywords(description, keywords):
    description = description.lower()  # Convert to lowercase for case-insensitive matching
    return any(keyword in description for keyword in keywords)

def recommend_movies_by_ratings(temperament, min_ratings=1):
    # Fetch temperament preferences
    temp_prefs = temperament_map[temperament]
    target_sentiments = temp_prefs['target_sentiments']
    print(temp_prefs)
    target_keywords = temp_prefs['keywords']

    # Filter by sentiment
    filtered_movies = movie_dataset[
        (movie_dataset['description'].apply(lambda x: match_keywords(str(x), target_keywords))) &
        (movie_dataset['sentiment_category'].isin(target_sentiments)) &
        (movie_dataset['rating'] >= min_ratings)  # Ensure sufficient reviews
    ]

    # Sort by rating and return top results
    return filtered_movies.sort_values(by='rating', ascending=False).head(100)


#Apply sentiment analysis
movie_dataset['sentiment_score'] = movie_dataset['description'].apply(lambda x: sentiment_analysis(str(x)))

movie_dataset['sentiment_category'] = movie_dataset['sentiment_score'].apply(categorize_sentiment)

temperament = 'melancholic'
recommended_movies = recommend_movies_by_ratings(temperament)
print(recommended_movies[['movie_name', 'genre', 'rating', 'sentiment_category']])
