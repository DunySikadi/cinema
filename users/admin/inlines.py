from ..models import Favorite
from django.contrib import admin


class FavoriteInline(admin.TabularInline):  
    model = Favorite
    extra = 1
    autocomplete_fields = ['film']
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(viewer=request.user)
    