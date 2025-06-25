from django.utils.html import format_html

def films_count(self, obj):
        return obj.films.count()
films_count.short_description = "Number of films" # type: ignore
    
def films_list(self, obj):
    films = obj.films.all()
    if not films:
        return "No related films"
    return format_html("<p>{}<p>", 
                          "".join(f"{film.title} ({film.release_date}), " 
                                  for film in films))
films_list.short_description = "Related films"  # type: ignore