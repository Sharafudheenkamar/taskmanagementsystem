# your_app/routing.py
from django.urls import re_path
from .consumers import TaskNotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/task_notifications/$', TaskNotificationConsumer.as_asgi()),
]
