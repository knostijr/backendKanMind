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
    ViewSet für Board CRUD-Operationen
    
    Endpoints:
    - GET /api/boards/ - Liste aller Boards
    - POST /api/boards/ - Board erstellen
    - GET /api/boards/{id}/ - Board-Details
    - PATCH /api/boards/{id}/ - Board aktualisieren
    - DELETE /api/boards/{id}/ - Board löschen
    - GET /api/email-check/ - Email verfügbar prüfen
    """
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        """
        Nutze DetailSerializer für einzelne Boards
        """
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardSerializer
    
    def get_queryset(self):
        """
        User sieht nur eigene Boards
        """
        return Board.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """
        Setze Owner automatisch auf aktuellen User
        """
        serializer.save(owner=self.request.user)
        
    @action(detail=False, methods=['get'])
    def email_check(self, request):
        """
        GET /api/email-check/
        Prüft ob eine E-Mail bereits registriert ist
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
    ViewSet für Task CRUD-Operationen
    
    Endpoints:
    - GET /api/tasks/ - Liste aller Tasks
    - POST /api/tasks/ - Task erstellen
    - GET /api/tasks/{id}/ - Task-Details
    - PATCH /api/tasks/{id}/ - Task aktualisieren
    - DELETE /api/tasks/{id}/ - Task löschen
    - GET /api/tasks/assigned-to-me/ - Mir zugewiesene Tasks
    - GET /api/tasks/reviewing/ - Tasks die ich reviewen soll
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskAssignedOrOwner]
    
    def get_serializer_class(self):
        """
        Nutze DetailSerializer für einzelne Tasks
        """
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer
    
    def get_queryset(self):
        """
        User sieht nur Tasks aus eigenen Boards
        oder Tasks die ihm zugewiesen sind
        """
        user = self.request.user
        return Task.objects.filter(
            board__owner=user
        ) | Task.objects.filter(
            assigned_to=user
        )
    
    @action(detail=False, methods=['get'])
    def assigned_to_me(self, request):
        """
        GET /api/tasks/assigned-to-me/
        Gibt alle Tasks zurück, die dem User zugewiesen sind
        """
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def reviewing(self, request):
        """
        GET /api/tasks/reviewing/
        Gibt alle Tasks zurück, die der User reviewen soll
        """
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet für Comment CRUD-Operationen
    
    Endpoints:
    - GET /api/tasks/{task_id}/comments/ - Alle Comments einer Task
    - POST /api/tasks/{task_id}/comments/ - Comment erstellen
    - DELETE /api/tasks/{task_id}/comments/{id}/ - Comment löschen
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]
    
    def get_queryset(self):
        """
        Filtere Comments nach Task
        """
        task_id = self.kwargs.get('task_pk')
        return Comment.objects.filter(task_id=task_id)
    
    def perform_create(self, serializer):
        """
        Setze Author und Task automatisch
        """
        task_id = self.kwargs.get('task_pk')
        serializer.save(
            author=self.request.user,
            task_id=task_id
        )