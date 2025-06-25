from rest_framework import serializers # type: ignore
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from .models import User, Favorite, FilmRating, AuthorRating

class FilmRatingSerializer(serializers.ModelSerializer):
    viewer = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = FilmRating
        fields = ['id', 'viewer', 'film', 'value', 'created_at']
        
class FavoriteSerializer(serializers.ModelSerializer):
    viewer = serializers.StringRelatedField(read_only=True)
    film = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'viewer', 'film', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'birth_date','role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            birth_date=validated_data.get('birth_date'),
            role='VIEWER'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class AuthorRatingSerializer(serializers.ModelSerializer):
    viewer = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = AuthorRating
        fields = ['id', 'viewer', 'author', 'value', 'created_at']
       
class UserSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription des spectateurs
    
    Validation:
        - Vérifie que les mots de passe correspondent
        - Valide le mot de passe avec les validateurs Django
    """
    ratings = AuthorRatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birth_date', 'bio', 'avatar','ratings']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
        }

# Creation d'une classe personnalisée pour le sérialiseur de token JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Cette méthode génère le token JWT pour l'utilisateur donné.
        
        Elle est appelée lorsqu'un utilisateur se connecte et que des identifiants valides sont fournis.
        On récupère d'abord le token standard généré par SimpleJWT,
        puis on y ajoute des informations supplémentaires (ex: rôle de l'utilisateur).
        """
        # Appel à la méthode parente pour obtenir un token standard (avec les champs de base : id, username, expirations, etc.)
        token = super().get_token(user)

        # information personnalisée au token : le rôle de l'utilisateur (ex: 'VIEWER', 'AUTHOR')
        # Cela permet d'utiliser cette donnée côté frontend ou dans les permissions Django REST Framework
        token['role'] = user.role

        # Retourne le token enrichi avec les informations personnalisées
        return token
    
    def validate(self, attrs):
        # Appel à la méthode parente pour obtenir les tokens
        data = super().validate(attrs)
        
        # On récupère l'utilisateur authentifié
        user = self.user

        # On ajoute les champs personnalisés dans la réponse JSON
        data['role'] = user.role
        
        return data