from django.utils import timezone
from datetime import datetime
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Task

timezone.now()
User = get_user_model()

@transaction.atomic
def create_task(
    *, 
    user: User, 
    title: str, 
    description: str = "", 
    priority: Task.Priority = Task.Priority.MEDIUM) -> Task:

    task = Task(
        user=user,
        title=title,
        description=description,
        priority=priority,
    )
    
    task.full_clean()
    task.save()
    return task

@transaction.atomic
def change_status(*, task: Task, new_status: Task.Status) -> Task:
    if task.status == new_status:
        return task

    if task.status == Task.Status.TODO and new_status == Task.Status.DONE:
        raise ValidationError({"status": "Task must be in progress before completion"})

    task.status = new_status
    task.full_clean()
    task.save(update_fields=["status","updated_at"])
    return task

def set_priority(*, task: Task, priority: Task.Priority) -> Task:
    task.priority = priority
    task.full_clean()
    task.save(update_fields=["priority","updated_at"])
    return task

def set_deadline(*, task: Task, deadline: datetime | None) -> Task:
    task.deadline = deadline
    task.full_clean()
    task.save(update_fields=["deadline", "updated_at"])
    return task

