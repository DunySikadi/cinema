from django.urls import path
from .views import FilmListView, FilmDetailView, ArchivedFilmListView

urlpatterns = [
    path('', FilmListView.as_view(), name='film-list'),
    path('archived/', ArchivedFilmListView.as_view(), name='archived-film-list'),
    path('<int:pk>/', FilmDetailView.as_view(), name='film-detail'),
]