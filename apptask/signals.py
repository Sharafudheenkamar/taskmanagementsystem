from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Task

@receiver(post_save, sender=Task)
def notify_task_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    message = f'Task "{instance.title}" has been {"created" if created else "updated"}.'

    async_to_sync(channel_layer.group_send)(
        'task_notifications',
        {
            'type': 'send_task_update',
            'title': instance.title,
            'message': message,
        }
    )
