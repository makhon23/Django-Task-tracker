from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.task_tracker.querysets import TaskQuerySet

User = get_user_model()


class Task(models.Model):
    objects = TaskQuerySet.as_manager()
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
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    deadline = models.DateTimeField(null=True, blank=True, db_index=True)
    class Meta:
        ordering = ["-created_at"]

    def clean(self) -> None:
        super().clean()
        self._validate_deadline()
        self._validate_status_rules()

    def _validate_deadline(self) -> None:
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError({"deadline": "Deadline cannot be in the past"})
        
    def _validate_status_rules(self) -> None:
        if self.status == self.Status.DONE and not self.description:
                raise ValidationError({"description": "Description required to complete Task"})

    def __str__(self) -> str:
        return f"[{self.get_status_display()}] {self.title}"
