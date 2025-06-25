from django.contrib import admin
from ..models import Film
from .filters import AverageRatingRangeFilter
from django.db.models import Avg
from .helpers import *

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'status', 'average_rating_display', 'is_from_tmdb')
    list_filter = ('status', 'created_at', AverageRatingRangeFilter)
    search_fields = ('title', 'description')
    filter_horizontal = ('authors',)
    readonly_fields = ('average_rating_display','authors_list')
    show_facets = admin.ShowFacets.ALWAYS # type: ignore
    
    fieldsets = (
        (None, {'fields': ('title', 'description', 'release_date','authors_list')}),
        ('Métadonnées', {'fields': ('authors', 'tmdb_id', 'is_from_tmdb')}),
        ('Statistiques', {'fields': ('average_rating_display',)}),
    )
        
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            average_rating=Avg('ratings__value')
        )
        
    # les méthodes définies plus haut  
    average_rating_display = average_rating_display
    authors_list = authors_list

    