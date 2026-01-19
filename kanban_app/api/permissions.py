# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Berechtigungsklasse für Objekte mit einem 'owner'-Feld (z.B. Boards).
    
    Ermöglicht jedem authentifizierten Benutzer den Lesezugriff. 
    Schreibzugriffe (PUT, PATCH, DELETE) sind ausschließlich dem 
    Besitzer des Objekts vorbehalten.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Prüft die Berechtigung für den Zugriff auf eine spezifische Objektinstanz.

        Args:
            request: Das aktuelle Request-Objekt.
            view: Die View, die den Zugriff anfordert.
            obj: Die Instanz des Models (z.B. ein Board), die geprüft wird.

        Returns:
            bool: True wenn Zugriff erlaubt, sonst False.
        """
        # SAFE_METHODS sind GET, HEAD und OPTIONS (reiner Lesezugriff)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Überprüfung, ob der anfragende User der im Modell hinterlegte Besitzer ist
        return obj.owner == request.user


class IsTaskAssignedOrOwner(permissions.BasePermission):
    """
    Erweiterte Berechtigungsklasse für Aufgaben (Tasks).
    
    Gewährt Lesezugriff für alle. Schreibrechte werden erteilt, wenn der 
    Benutzer entweder:
    1. Der Besitzer des Boards ist, zu dem die Task gehört.
    2. Der explizit zugewiesene Bearbeiter (assigned_to) der Task ist.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Prüft die Schreibrechte basierend auf Board-Besitz oder Task-Zuweisung.
        """
        # Lesezugriff ist für autorisierte User immer gestattet
        if request.method in permissions.SAFE_METHODS:
            return True

        # Prüfung der zwei erlaubten Rollen für Modifikationen
        return (
            obj.board.owner == request.user or
            obj.assigned_to == request.user
        )


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Berechtigungsklasse für Kommentare.
    
    Stellt sicher, dass Kommentare von jedem gelesen, aber nur vom 
    ursprünglichen Verfasser (Author) bearbeitet oder gelöscht werden können.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Prüft, ob der aktuelle Benutzer der Autor des Kommentars ist.
        """
        # Lesezugriff für alle authentifizierten User
        if request.method in permissions.SAFE_METHODS:
            return True

        # Schreibzugriff nur für den Ersteller des Kommentars
        return obj.author == request.user