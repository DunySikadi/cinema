from django.contrib.admin import SimpleListFilter
from django.contrib import admin


class AverageRatingRangeFilter(admin.SimpleListFilter):
    title = 'Note moyenne'
    parameter_name = 'avg_rating'

    def lookups(self, request, model_admin):
        return [
            ('lt_6', 'Moins de 6'),
            ('6_to_8', 'Entre 6 et 8'),
            ('ge_8', '8 et plus'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'lt_6':
            return queryset.filter(average_rating__lt=6)
        elif self.value() == '6_to_8':
            return queryset.filter(average_rating__gte=6, average_rating__lt=8)
        elif self.value() == 'ge_8':
            return queryset.filter(average_rating__gte=8)
        return queryset