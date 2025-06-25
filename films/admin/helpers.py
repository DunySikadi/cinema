from django.db.models import Avg
from django.utils.html import format_html

def authors_list(self, obj):
        authors = obj.authors.all()
        if not authors:
            return "No related authors"
        return format_html("<p>{}<p>", 
                          "".join(f"{author.username} (author rating: {author.average_rating()}), " 
                                  for author in authors))
authors_list.short_description = "Related authors" # type: ignore

def average_rating_display(self, obj):
    if hasattr(obj, 'average_rating') and obj.average_rating is not None:
        return round(obj.average_rating, 1)
    return "Aucune"
average_rating_display.short_description = "Note moyenne" # type: ignore
average_rating_display.admin_order_field = 'average_rating' # type: ignore