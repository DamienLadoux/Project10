from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    L'auteur d'une ressource peut la modifier ou la supprimer.
    Les autres utilisateurs peuvent uniquement la consulter.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsProjectContributor(BasePermission):
    """
    Autorise uniquement les utilisateurs qui sont contributeurs
    du projet concerné.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.project.contributors.filter(user=request.user).exists()
