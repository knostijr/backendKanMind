# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Lokale Importe
from kanban_app.models import Board, Comment, Task
from .permissions import (
    IsCommentAuthorOrReadOnly,
    IsOwnerOrReadOnly,
    IsTaskAssignedOrOwner
)
from .serializers import (
    BoardDetailSerializer,
    BoardSerializer,
    CommentSerializer,
    TaskDetailSerializer,
    TaskSerializer
)


class BoardViewSet(viewsets.ModelViewSet):
    """
    Schnittstelle für die Verwaltung von Kanban-Boards.

    Bietet standardmäßige CRUD-Operationen und stellt sicher, dass Benutzer 
    nur Zugriff auf ihre eigenen Boards haben.
    """
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        """
        Wählt den Serializer basierend auf der Aktion aus.
        
        Gibt BoardDetailSerializer für Detailansichten zurück, um tiefer 
        verschachtelte Daten (wie Tasks) anzuzeigen.
        """
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardSerializer

    def get_queryset(self):
        """
        Filtert die Boards so, dass nur die vom aktuellen Benutzer 
        erstellten Boards zurückgegeben werden.
        """
        return Board.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Verknüpft das neue Board beim Speichern automatisch mit dem 
        aktuell angemeldeten Benutzer als Besitzer.
        """
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def email_check(self, request):
        """
        Überprüft die Verfügbarkeit einer E-Mail-Adresse.

        Query-Parameter:
            ?email=<adresse>

        Returns:
            Response: Ein Boolean 'available', der angibt, ob die E-Mail noch frei ist.
        """
        email = request.query_params.get('email', None)
        if not email:
            return Response(
                {"error": "Email parameter required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.contrib.auth.models import User
        exists = User.objects.filter(email=email).exists()

        return Response({"available": not exists})


class TaskViewSet(viewsets.ModelViewSet):
    """
    Schnittstelle für die Aufgabenverwaltung.

    Ermöglicht das Erstellen, Bearbeiten und Filtern von Aufgaben innerhalb 
    verschiedener Boards. Unterstützt spezielle Ansichten für zugewiesene Aufgaben.
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskAssignedOrOwner]

    def get_serializer_class(self):
        """
        Wählt TaskDetailSerializer für die Einzelansicht, um zusätzliche 
        Informationen wie Kommentare einzuschließen.
        """
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer

    def get_queryset(self):
        """
        Bestimmt die sichtbaren Aufgaben für den Benutzer.
        
        Ein Benutzer sieht Aufgaben, wenn er entweder der Besitzer des 
        entsprechenden Boards oder der Bearbeiter (assigned_to) der Aufgabe ist.
        """
        user = self.request.user
        return Task.objects.filter(
            board__owner=user
        ) | Task.objects.filter(
            assigned_to=user
        )

    @action(detail=False, methods=['get'], url_path='assigned-to-me')
    def assigned_to_me(self, request):
        """
        Filtert alle Aufgaben, die dem aktuell angemeldeten Benutzer 
        zugewiesen wurden.
        """
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def reviewing(self, request):
        """
        Gibt eine Liste von Aufgaben zurück, bei denen der aktuelle 
        Benutzer als Reviewer eingetragen ist.
        """
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Schnittstelle für Kommentare zu Aufgaben.

    Diese View ist für die Nutzung mit verschachtelten Routern optimiert 
    (Nested Routes), um Kommentare direkt unterhalb einer Task-ID zu verwalten.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        """
        Extrahiert die task_id aus der URL-Struktur, um nur Kommentare 
        der spezifischen Aufgabe anzuzeigen.
        """
        task_id = self.kwargs.get('task_pk')
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        """
        Speichert einen neuen Kommentar und verknüpft ihn automatisch 
        mit dem angemeldeten Benutzer und der Aufgabe aus der URL.
        """
        task_id = self.kwargs.get('task_pk')
        serializer.save(
            author=self.request.user,
            task_id=task_id
        )
