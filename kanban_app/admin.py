# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from django.contrib import admin

# Lokale Importe
from .models import Board, Comment, Task


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    list_filter = ['owner', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'board',
        'status',
        'priority',
        'assigned_to',
        'due_date'
    ]
    list_filter = ['status', 'priority', 'board', 'assigned_to']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'task', 'text', 'created_at']
    list_filter = ['author', 'created_at']
    search_fields = ['text']
    date_hierarchy = 'created_at'
