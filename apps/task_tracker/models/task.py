from django.contrib.auth import get_user_model
from django.db import models

from apps.task_tracker.querysets import TaskQuerySet

User = get_user_model()


class Task(models.Model):
    object = TaskQuerySet.as_manager()

    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.TODO, 
        db_index=True
    )

    priority = models.IntegerField(
        choices=Priority.choices, 
        default=Priority.MEDIUM, 
        db_index=True
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="tasks", 
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"
