from django.core.management.base import BaseCommand
from recommender.models import Movie
import pandas as pd
import ast
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Import movies from TMDB dataset'
    
    def handle(self, *args, **kwargs):
        # Load dataset
        data_path = os.path.join(settings.DATA_DIR, 'tmdb_5000_movies.csv')
        df = pd.read_csv(data_path)
        
        # Print columns for debugging
        self.stdout.write(f"Dataset columns: {', '.join(df.columns)}")
        
        # Helper function to parse genres
        def parse_genres(genre_str):
            try:
                genres = ast.literal_eval(genre_str)
                return [g['name'] for g in genres]
            except:
                return []
        
        # Import movies
        total_count = 0
        for index, row in df.iterrows():
            # Skip if title is missing
            title = row.get('title') or row.get('original_title')
            if not title or pd.isna(title):
                continue
                
            # Handle different column names for rating
            rating = row.get('vote_average') or row.get('rating') or 0.0
            if pd.isna(rating):
                rating = 0.0
                
            # Handle poster path variations
            poster_path = row.get('poster_path') or row.get('poster')
            poster_url = ""
            if poster_path and not pd.isna(poster_path):
                poster_path = str(poster_path).strip()
                if poster_path.startswith('/'):
                    poster_path = poster_path[1:]
                poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            
            # Handle overview
            overview = row.get('overview', '')
            if pd.isna(overview):
                overview = ''
                
            # Handle genres
            genres = parse_genres(row.get('genres', ''))
            
            # Use update_or_create to handle duplicates
            Movie.objects.update_or_create(
                title=title,
                defaults={
                    'genres': genres,
                    'keywords': '',
                    'overview': overview,
                    'rating': rating,
                    'poster_url': poster_url
                }
            )
            
            total_count += 1
            if total_count % 100 == 0:
                self.stdout.write(f"Imported {total_count} movies")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully imported {total_count} movies"))