from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .filters import HasFilmsFilter
from .helpers import *
from ..models import AuthorRating,FilmRating,Favorite
from .inlines import FavoriteInline

# Récuperation du model user personnalisé
User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'birth_date', 'is_staff','films_count',)
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', HasFilmsFilter)
    readonly_fields = ('films_list',)
    inlines = [FavoriteInline]
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'role', 'birth_date', 'is_staff','films_list')
        }),
    )
    show_facets = admin.ShowFacets.ALWAYS # type: ignore
    
    # les méthodes définies plus haut
    films_count = films_count
    films_list = films_list

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if obj and obj.role == User.Role.VIEWER: # type: ignore
            return inline_instances
        return []

@admin.register(AuthorRating)
class AuthorRatingAdmin(admin.ModelAdmin):
    list_display = ('viewer','author', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('viewer__username', 'author__username')

@admin.register(FilmRating)
class FilmRatingAdmin(admin.ModelAdmin):
    list_display = ('viewer', 'film', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('viewer__username', 'film__title')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('viewer', 'film', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('viewer__username', 'film__title')
