from datetime import datetime
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

def create_task(*, user: User, title: str, description: str = "", priority: int) -> Task:
	task = Task(
		user=user,
		title=title,
		description=description,
		priority=priority,
)
	task.full_clean()
	task.save()
	return task 

def change_status(*, task: Task, status: Task.Status) -> Task:
	task.status = status
	task.full_clean()
	task.save(update_fields=["status"])
	return task

def set_priority(*, task: Task, priority: Task.Priority) -> Task:
	task.priority = priority
	task.full_clean()
	task.save(update_fields=["priority"])
	return task

def set_deadline(*, task: Task, deadline: datetime | None) -> Task:
	task.deadline = deadline
	task.full_clean()
	task.save(update_fields=["deadline"])
	return task