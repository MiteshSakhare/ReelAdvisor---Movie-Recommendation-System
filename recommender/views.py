from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from .utils import train_model, get_recommendations
import pandas as pd
import sys
import os
import ast
import numpy as np
import os
from django.conf import settings
from django.shortcuts import render
# ... other imports
from PIL import Image, ImageDraw, ImageFont

# Create placeholder image if missing
def create_placeholder_image():
    placeholder_path = os.path.join(settings.BASE_DIR, 'recommender', 'static', 'img', 'placeholder.png')
    if not os.path.exists(placeholder_path):
        # Create directory if needed
        os.makedirs(os.path.dirname(placeholder_path), exist_ok=True)
        
        # Create image
        img = Image.new('RGB', (300, 450), color=(30, 41, 59))
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = "No Poster"
        text_width, text_height = draw.textsize(text, font=font)
        position = ((300 - text_width) // 2, (450 - text_height) // 2)
        
        draw.text(position, text, fill=(255, 255, 255), font=font)
        img.save(placeholder_path)

# Call this when server starts
create_placeholder_image()

# Global variables for model
cosine_sim = None
indices = None
df = None

# Load model when server starts
if 'runserver' in sys.argv or 'shell' in sys.argv:
    try:
        print("Loading recommendation model...")
        cosine_sim, indices, df = train_model()
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

def home(request):
    return render(request, 'index.html')

def recommend(request):
    global cosine_sim, indices, df
    
    # Check if model is loaded
    if cosine_sim is None or indices is None or df is None:
        return render(request, 'index.html', {'error': 'Recommendation model is not available. Please restart the server.'})
    
    if request.method == 'POST':
        movie_title = request.POST.get('movie', '').strip()
        if not movie_title:
            return render(request, 'index.html', {'error': 'Please enter a movie title.'})
        
        try:
            recommendations = get_recommendations(movie_title, cosine_sim, indices, df)
            
            if recommendations.empty:
                return render(request, 'index.html', {'error': 'Movie not found. Please try another title.'})
            
            movies = []
            for _, row in recommendations.iterrows():
                # Handle poster URL properly
                poster_url = ""
                if 'poster_path' in row and not pd.isna(row['poster_path']):
                    poster_path = str(row['poster_path']).strip()
                    if poster_path.startswith('/'):
                        poster_path = poster_path[1:]
                    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                
                # Handle genres properly
                genres = []
                if 'genres' in row and not pd.isna(row['genres']):
                    if isinstance(row['genres'], str):
                        try:
                            genres_data = ast.literal_eval(row['genres'])
                            genres = [g['name'] for g in genres_data]
                        except:
                            genres = []
                    else:
                        genres = row['genres']
                
                # Create or update movie
                movie, created = Movie.objects.update_or_create(
                    title=row['title'],
                    defaults={
                        'genres': genres,
                        'keywords': row.get('keywords', ''),
                        'overview': row['overview'] if pd.notna(row['overview']) else '',
                        'rating': row['vote_average'] if not pd.isna(row['vote_average']) else 0.0,
                        'poster_url': poster_url
                    }
                )
                movies.append(movie)
            
            return render(request, 'recommendations.html', {
                'movies': movies,
                'search_movie': movie_title
            })
        
        except Exception as e:
            return render(request, 'index.html', {'error': f'Error: {str(e)}'})
    
    return render(request, 'index.html')

def autocomplete(request):
    term = request.GET.get('term', '')
    movies = Movie.objects.filter(title__icontains=term)[:10]
    suggestions = [movie.title for movie in movies]
    return JsonResponse(suggestions, safe=False)