from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from .models import User, Favorite, AuthorRating,FilmRating
from .permissions import IsViewerPermission
from .serializers import (
    UserSerializer, RegisterSerializer, 
    CustomTokenObtainPairSerializer, AuthorRatingSerializer, FilmRatingSerializer, FavoriteSerializer
)
from films.models import Film
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework.views import APIView # type: ignore

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
class LogoutView(APIView):
    """
    Vue pour gérer la déconnexion des utilisateurs.
    Invalide le refresh token pour empêcher son utilisation future.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Reçoit un refresh token et le blacklist.
        """
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Le champ 'refresh_token' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(
                {"detail": "Token invalide ou déjà blacklisté."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(
            {"detail": "Déconnexion réussie."},
            status=status.HTTP_205_RESET_CONTENT
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(role=User.Role.AUTHOR)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role=User.Role.AUTHOR)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def patch(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            print(f"Erreur PATCH: {str(e)}")  # Log dans la console
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.films.exists():
            return Response(
                {"detail": "Impossible de supprimer un auteur ayant des films."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthorRatingCreateView(generics.CreateAPIView):
    queryset = AuthorRating.objects.all()
    serializer_class = AuthorRatingSerializer
    permission_classes = [IsViewerPermission]
    
    def perform_create(self, serializer):
        serializer.save(viewer=self.request.user)
        
class FilmRatingCreateView(generics.CreateAPIView):
    queryset = FilmRating.objects.all()
    serializer_class = FilmRatingSerializer
    permission_classes = [IsViewerPermission]
    
    def perform_create(self, serializer):
        serializer.save(viewer=self.request.user)

class FavoriteListView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsViewerPermission]
    
    def get_queryset(self):
        return Favorite.objects.filter(viewer=self.request.user)
    
    def perform_create(self, serializer):
        film_id = self.request.data.get('film')
        try:
            film = Film.objects.get(pk=film_id)
            serializer.save(viewer=self.request.user, film=film)
        except Film.DoesNotExist:
            raise serializers.ValidationError({"film": "Film introuvable."}) # type: ignore

class FavoriteDetailView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsViewerPermission]
    
    def get_object(self):
        return get_object_or_404(Favorite, pk=self.kwargs["pk"], viewer=self.request.user)