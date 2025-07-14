from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, CustomTokenObtainPairView,
    UserListView, UserDetailView, AuthorRatingCreateView,
    FilmRatingCreateView, FavoriteListView, FavoriteDetailView,LogoutView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('authors/', UserListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', UserDetailView.as_view(), name='author-detail'),
    
    path('ratings/author', AuthorRatingCreateView.as_view(), name='rating-create-author'),
    path('ratings/film', FilmRatingCreateView.as_view(), name='rating-create-film'),
    
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/<int:pk>/', FavoriteDetailView.as_view(), name='favorite-detail'),
]