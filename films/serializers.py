from rest_framework import serializers # type: ignore
from users.serializers import UserSerializer
from .models import Film
from users.serializers import FilmRatingSerializer
    
class FilmSerializer(serializers.ModelSerializer):
    authors = UserSerializer(many=True, read_only=True)
    ratings = FilmRatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Film
        fields = [
            'id', 'title', 'description', 'release_date','status', 'authors', 'ratings',
            'created_at', 'updated_at', 'is_from_tmdb'
        ]

class FilmCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = [
            'id', 'title', 'description', 'release_date','status', 'authors', 'tmdb_id', 'is_from_tmdb'
        ]
        extra_kwargs = {
            'tmdb_id': {'required': False},
            'is_from_tmdb': {'required': False},
        }