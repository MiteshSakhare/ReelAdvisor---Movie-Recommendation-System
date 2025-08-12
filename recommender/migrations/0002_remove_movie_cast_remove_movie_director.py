from django.db import migrations

def remove_duplicate_movies(apps, schema_editor):
    Movie = apps.get_model('recommender', 'Movie')
    titles = Movie.objects.values_list('title', flat=True).distinct()
    
    for title in titles:
        movies = Movie.objects.filter(title=title)
        if movies.count() > 1:
            # Keep the first instance and delete duplicates
            first = movies.first()
            movies.exclude(id=first.id).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate_movies),
    ]