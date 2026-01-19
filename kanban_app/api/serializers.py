# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from rest_framework import serializers

# Lokale Importe
from kanban_app.models import Board, Comment, Task


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer für Kommentar-Objekte.
    
    Zusätzlich zu den Basisdaten wird der Benutzername des Autors 
    über eine ReadOnly-Quelle eingebunden, um die Frontend-Anzeige zu erleichtern.
    """
    author_username = serializers.ReadOnlyField(
        source='author.username'
    )

    class Meta:
        """Konfiguration des CommentSerializers."""
        model = Comment
        fields = [
            'id',
            'task',
            'author',
            'author_username',
            'text',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    """
    Basis-Serializer für Aufgaben (Tasks).
    
    Beinhaltet Informationen zu Bearbeitern, Reviewern und eine 
    zusammenfassende Anzahl der vorhandenen Kommentare.
    """
    assigned_to_username = serializers.ReadOnlyField(
        source='assigned_to.username'
    )
    reviewer_username = serializers.ReadOnlyField(
        source='reviewer.username'
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        """Konfiguration des TaskSerializers."""
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assigned_to',
            'assigned_to_username',
            'reviewer',
            'reviewer_username',
            'due_date',
            'created_at',
            'updated_at',
            'comments_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        """
        Berechnet die Gesamtzahl der Kommentare, die mit dieser Task verknüpft sind.
        
        Args:
            obj (Task): Die aktuelle Task-Instanz.
        """
        return obj.comments.count()


class TaskDetailSerializer(TaskSerializer):
    """
    Detaillierte Ansicht einer Aufgabe.
    
    Erweitert den Basis-TaskSerializer um die vollständige Liste 
    aller zugehörigen Kommentare (verschachtelte Serialisierung).
    """
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(TaskSerializer.Meta):
        """Erweitert die Meta-Felder der Basis-Klasse um die 'comments'."""
        fields = TaskSerializer.Meta.fields + ['comments']


class BoardSerializer(serializers.ModelSerializer):
    """
    Basis-Serializer für Kanban-Boards.
    
    Liefert Eckdaten zum Board sowie die Anzahl der enthaltenen Aufgaben zurück.
    """
    owner_username = serializers.ReadOnlyField(
        source='owner.username'
    )
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        """Konfiguration des BoardSerializers."""
        model = Board
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'owner_username',
            'created_at',
            'updated_at',
            'tasks_count'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def get_tasks_count(self, obj):
        """
        Berechnet die Anzahl der Aufgaben innerhalb dieses Boards.
        
        Args:
            obj (Board): Die aktuelle Board-Instanz.
        """
        return obj.tasks.count()


class BoardDetailSerializer(BoardSerializer):
    """
    Detaillierte Ansicht eines Boards.
    
    Erweitert den BoardSerializer um eine Liste aller enthaltenen Tasks. 
    Wird typischerweise in der Detail-Abfrage (Retrieve) genutzt.
    """
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta(BoardSerializer.Meta):
        """Erweitert die Meta-Felder der Basis-Klasse um die 'tasks'."""
        fields = BoardSerializer.Meta.fields + ['tasks']