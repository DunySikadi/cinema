from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint, Avg
from django.core.exceptions import ValidationError



class User(AbstractUser):
    class Role(models.TextChoices):
        AUTHOR = 'AUTHOR', 'Auteur'
        VIEWER = 'VIEWER', 'Spectateur'
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    def average_rating(self):
        result = self.ratings.aggregate( # type: ignore
            average=Avg('value'),
            )
        avg = result['average']
        return round(avg, 1) if avg is not None else None
            
class FilmRating(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='film_ratings')
    film = models.ForeignKey('films.Film', on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['viewer', 'film'], 
                name='unique_viewer_film_rating'
            )
        ]
        verbose_name = "Note de film"
        verbose_name_plural = "Notes de films"

    def __str__(self):
        return f"{self.viewer.username} - {self.film.title}: {self.value}"
    
    def clean(self):
        """
        Effectue des validations métier personnalisées sur les données du formulaire.
        Cette méthode vérifie que l'utilisateur associé à la note 
        a bien le rôle 'VIEWER', car seuls les spectateurs sont autorisés 
        à attribuer une note à un film.
        
        Raises:
            ValidationError: Si l'utilisateur n'a pas le rôle 'VIEWER'.
        """
        if self.viewer.role != User.Role.VIEWER:
            raise ValidationError("Seuls les spectateurs peuvent ajouter une note.")
        super().clean()

class AuthorRating(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['viewer', 'author'], 
                name='unique_viewer_author_rating'
            )
        ]
        verbose_name = "Note d'auteur"
        verbose_name_plural = "Notes d'auteurs"

    def __str__(self):
        return f"{self.viewer.username} - {self.author.username}: {self.value}"
    
    def clean(self):
        """
        Effectue des validations métier personnalisées sur les données du formulaire.
        Cette méthode vérifie que l'utilisateur associé à la note 
        a bien le rôle 'VIEWER', car seuls les spectateurs sont autorisés 
        à attribuer une note à un film.
        
        Raises:
            ValidationError: Si l'utilisateur n'a pas le rôle 'VIEWER'.
        """
        if self.viewer.role != User.Role.VIEWER:
            raise ValidationError("Seuls les spectateurs peuvent ajouter une note.")
        super().clean()

class Favorite(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    film = models.ForeignKey('films.Film', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Un utilisateur ne peut pas mettre en favoris deux fois le même film
        UniqueConstraint(fields=['viewer', 'film'], name='unique_viewer_film') 
    
    def __str__(self):
        return f"{self.viewer.username} aime {self.film.title}"
    
    def clean(self):
        """
        Effectue des validations métier personnalisées sur les données du formulaire.
        Cette méthode vérifie que l'utilisateur associé à la note 
        a bien le rôle 'VIEWER', car seuls les spectateurs sont autorisés 
        à apprécier un film.
        
        Raises:
            ValidationError: Si l'utilisateur n'a pas le rôle 'VIEWER'.
        """
        if self.viewer.role != User.Role.VIEWER:
            raise ValidationError("Seuls les spectateurs peuvent apprécier un film.")
        super().clean()