import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.conf import settings
import os
import ast

def load_and_preprocess_data():
    """Load and preprocess the dataset"""
    data_path = os.path.join(settings.DATA_DIR, 'tmdb_5000_movies.csv')
    df = pd.read_csv(data_path)
    
    # Handle missing data
    df['overview'] = df['overview'].fillna('')
    df['genres'] = df['genres'].fillna('[]')
    df['keywords'] = df['keywords'].fillna('[]')
    
    # Parse JSON columns
    def parse_json_column(column):
        try:
            return ast.literal_eval(column)
        except:
            return []
    
    df['genres'] = df['genres'].apply(parse_json_column)
    df['keywords'] = df['keywords'].apply(parse_json_column)
    
    # Extract genre names
    df['genres'] = df['genres'].apply(lambda x: ' '.join([g['name'] for g in x]))
    df['keywords'] = df['keywords'].apply(lambda x: ' '.join([k['name'] for k in x]))
    
    # Combine features
    df['combined_features'] = df['genres'] + " " + df['keywords'] + " " + df['overview']
    
    return df

def train_model():
    """Train the recommendation model"""
    df = load_and_preprocess_data()
    
    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    # Compute cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # Create title-index mapping
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    
    return cosine_sim, indices, df

def get_recommendations(title, cosine_sim, indices, df):
    """Get top 10 recommendations for a movie"""
    try:
        idx = indices[title]
    except KeyError:
        return pd.DataFrame()  # Return empty if movie not found
    
    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort movies by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 10 similar movies (excluding itself)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    
    return df.iloc[movie_indices]