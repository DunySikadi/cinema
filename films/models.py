from django.db import models
from django.db.models import Avg
from users.models import User

class Film(models.Model):
     
    class Statut(models.TextChoices):
        IN_PRODUCTION = 'IN_PRODUCTION', 'En production'
        POST_PRODUCTION = 'POST_PRODUCTION', 'Post-production'
        COMING_SOON = 'COMING_SOON', 'À venir'
        NOW_SHOWING = 'NOW_SHOWING', 'En salle'
        RELEASED = 'RELEASED', 'Sorti'
        ARCHIVED = 'ARCHIVED', 'Archivé'
        CANCELLED = 'CANCELLED', 'Annulé'
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    status = models.CharField(max_length=30, choices=Statut.choices, default=Statut.IN_PRODUCTION)
    authors = models.ManyToManyField(User, related_name='films')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tmdb_id = models.IntegerField(null=True, blank=True, unique=True)
    is_from_tmdb = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def average_rating(self):
        result = self.ratings.aggregate(average=Avg('value'))  # type: ignore
        avg = result.get('average')
        return round(avg, 1) if avg is not None else None