from rest_framework import generics, permissions 
from django_filters.rest_framework import DjangoFilterBackend 
from .models import Film
from .serializers import FilmSerializer, FilmCreateSerializer

class FilmListView(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]  # type: ignore
    filterset_fields = ['status', 'is_from_tmdb']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FilmCreateSerializer
        return FilmSerializer

class FilmDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_destroy(self, instance):
        instance.status = Film.Statut.ARCHIVED
        instance.save()

class ArchivedFilmListView(generics.ListAPIView):
    queryset = Film.objects.filter(status=Film.Statut.ARCHIVED)
    serializer_class = FilmSerializer
    permission_classes = [permissions.AllowAny]