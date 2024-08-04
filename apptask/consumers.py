# your_app/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class TaskNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass

    def send_task_update(self, title, message):
        self.send(text_data=json.dumps({
            'title': title,
            'message': message,
        }))
