# Standardbibliothek
# (keine benötigt)

# Drittanbieter (Third-party)
from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    """
    Repräsentiert ein Kanban-Board innerhalb der Anwendung.
    
    Ein Board dient als Container für Tasks und ist immer einem spezifischen 
    Besitzer (User) zugeordnet. Löscht man den User, werden auch alle 
    seine Boards gelöscht (CASCADE).
    """
    title = models.CharField(max_length=200, help_text="Der Name des Boards.")
    description = models.TextField(blank=True, help_text="Optionale Beschreibung des Zwecks.")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="boards",
        help_text="Der Benutzer, dem dieses Board gehört."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metadaten für das Board-Model.
        Sortiert standardmäßig nach dem Erstellungsdatum (neueste zuerst).
        """
        ordering = ['-created_at']
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

    def __str__(self):
        """Gibt eine lesbare Zeichenkette für das Board zurück."""
        return f"{self.title} (Owner: {self.owner.username})"


class Task(models.Model):
    """
    Repräsentiert eine einzelne Aufgabe innerhalb eines Boards.
    
    Tasks enthalten Status- und Prioritätsinformationen und können 
    sowohl einem Bearbeiter (assigned_to) als auch einem Prüfer (reviewer) 
    zugewiesen werden.
    """
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="Das Board, zu dem diese Aufgabe gehört."
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        help_text="Benutzer, der die Aufgabe bearbeitet."
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_tasks",
        help_text="Benutzer, der das Ergebnis der Aufgabe prüft."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True, help_text="Optionales Fälligkeitsdatum.")

    class Meta:
        """
        Metadaten für das Task-Model.
        Sortiert standardmäßig nach dem Erstellungsdatum.
        """
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        """Gibt eine lesbare Zeichenkette für die Task zurück."""
        return f"{self.title} ({self.status})"


class Comment(models.Model):
    """
    Repräsentiert einen Kommentar zu einer spezifischen Aufgabe.
    
    Ermöglicht die Kommunikation zwischen Teammitgliedern innerhalb einer Task.
    Wird die Task oder der Autor gelöscht, verschwindet auch der Kommentar (CASCADE).
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Die Aufgabe, die kommentiert wird."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Der Verfasser des Kommentars."
    )
    text = models.TextField(help_text="Der eigentliche Inhalt des Kommentars.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metadaten für das Comment-Model.
        Zeigt immer die neuesten Kommentare oben an.
        """
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """Gibt eine kurze Zusammenfassung des Kommentars zurück."""
        return f"Comment by {self.author.username} on {self.task.title}"
