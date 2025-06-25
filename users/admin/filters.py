from django.contrib import admin

class HasFilmsFilter(admin.SimpleListFilter):
    """
    Filtre personnalisé pour l'interface admin qui permet de filtrer les utilisateurs
    selon s'ils ont des films associés ou non.
    """
    # Titre qui apparaîtra dans l'interface d'administration
    title = 'has films'
    # Le paramètre qui sera utilisé dans l'URL pour ce filtre
    parameter_name = 'has_films'

    def lookups(self, request, model_admin):
        """
        Définit les choix disponibles dans le filtre.
        Retourne un tuple de tuples (valeur, libellé).
        """
        return [
            ('yes', 'Oui'),  # Option pour les utilisateurs AVEC films
            ('no', 'Non'),   # Option pour les utilisateurs SANS films
        ]

    def queryset(self, request, queryset):
        """
        Applique le filtre au queryset en fonction de la sélection.
        
        Args:
            request: L'objet HttpRequest
            queryset: Le queryset initial à filtrer
            
        Returns:
            Queryset filtré selon la sélection
        """
        # Si 'Oui' est sélectionné (utilisateurs avec films)
        if self.value() == 'yes':
            return queryset.filter(films__isnull=False).distinct()
        
        # Si 'Non' est sélectionné (utilisateurs sans films)
        if self.value() == 'no':
            return queryset.filter(films__isnull=True)
        
        # Si aucun filtre n'est sélectionné, retourne le queryset original
        return queryset