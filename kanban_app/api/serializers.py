# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from rest_framework import serializers

# Lokale Importe
from kanban_app.models import Board, Comment, Task


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer für Comments
    """
    author_username = serializers.ReadOnlyField(
        source='author.username'
    )
    
    class Meta:
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
    Serializer für Tasks
    """
    assigned_to_username = serializers.ReadOnlyField(
        source='assigned_to.username'
    )
    reviewer_username = serializers.ReadOnlyField(
        source='reviewer.username'
    )
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
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
        Zähle Anzahl der Comments für diese Task
        """
        return obj.comments.count()


class TaskDetailSerializer(TaskSerializer):
    """
    Detaillierter Task-Serializer mit allen Comments
    """
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['comments']


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer für Boards
    """
    owner_username = serializers.ReadOnlyField(
        source='owner.username'
    )
    tasks_count = serializers.SerializerMethodField()
    
    class Meta:
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
        Zähle Anzahl der Tasks in diesem Board
        """
        return obj.tasks.count()


class BoardDetailSerializer(BoardSerializer):
    """
    Detaillierter Board-Serializer mit allen Tasks
    """
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta(BoardSerializer.Meta):
        fields = BoardSerializer.Meta.fields + ['tasks']