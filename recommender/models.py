from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    genres = models.JSONField(default=list, blank=True)  # Store as list of strings
    keywords = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title