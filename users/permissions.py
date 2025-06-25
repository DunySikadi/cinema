from rest_framework import permissions # type: ignore

class IsViewerPermission(permissions.BasePermission):
    """
    Permet uniquement aux utilisateurs ayant le rôle 'VIEWER' d'accéder à la vue.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est connecté
        if not request.user.is_authenticated:
            return False
        
        # Vérifie si l'utilisateur a le rôle 'VIEWER'
        return getattr(request.user, 'role', None) == 'VIEWER'