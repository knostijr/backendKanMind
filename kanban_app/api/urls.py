# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# Lokale Importe
from .views import BoardViewSet, CommentViewSet, TaskViewSet

"""
URL-Konfiguration für die Kanban-API.

Hier wird das Routing für die Hauptressourcen (Boards, Tasks) sowie 
die verschachtelten Ressourcen (Comments innerhalb von Tasks) definiert.
"""

# Haupt-Router für die Top-Level Ressourcen
# Erstellt automatisch Routen für:
# /api/boards/ und /api/tasks/
router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'tasks', TaskViewSet, basename='task')

# Konfiguration des Nested Routers für Kommentare
# Erzeugt eine Hierarchie, in der Kommentare immer einer Task untergeordnet sind.
# Die 'lookup' Angabe 'task' führt dazu, dass in der URL die Variable 'task_pk' 
# an das ViewSet übergeben wird.
tasks_router = routers.NestedDefaultRouter(
    router,
    r'tasks',
    lookup='task'
)
# Registrierung der Kommentare unterhalb des Task-Pfades
# Resultierende URL-Struktur: /api/tasks/{task_pk}/comments/
tasks_router.register(
    r'comments',
    CommentViewSet,
    basename='task-comments'
)

# Zusammenführung aller URL-Muster
urlpatterns = [
    # Bindet die Standard-Routen für Boards und Tasks ein
    path('', include(router.urls)),
    
    # Bindet die verschachtelten Routen für die Kommentare ein
    path('', include(tasks_router.urls)),
]
