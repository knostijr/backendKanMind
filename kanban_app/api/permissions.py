from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom Permission:
    - Owner kann alles machen
    - Andere können nur lesen
    """
    def has_object_permission(self, request, view, obj):
        # Lesezugriff für alle authentifizierten User
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Schreibzugriff nur für Owner
        return obj.owner == request.user

class IsTaskAssignedOrOwner(permissions.BasePermission):
    """
    Custom Permission für Tasks:
    - Board-Owner kann alles
    - Assigned User kann Task bearbeiten
    """
    def has_object_permission(self, request, view, obj):
        # Lesezugriff für alle
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Schreibzugriff für Board-Owner oder Assigned User
        return (
            obj.board.owner == request.user or
            obj.assigned_to == request.user
        )
        
class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom Permission für Comments:
    - Autor kann Comment bearbeiten/löschen
    - Andere können nur lesen
    """
    def has_object_permission(self, request, view, obj):
        # Lesezugriff für alle
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Schreibzugriff nur für Autor
        return obj.author == request.user