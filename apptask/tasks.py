from celery import shared_task
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_notification(email, task_id):
    try:
        task = Task.objects.get(id=task_id)
        send_mail(
            'New Task Assigned',
            f'You have been assigned a new task: {task.title}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
    except Task.DoesNotExist:
        # Handle the case where the task does not exist
        pass
