import asyncio

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
import json

from .models import Author, PrivateRoom, PrivateMessage, User


class ChatConsumer(WebsocketConsumer):



    def connect(self):
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)


    def receive(self, text_data):

        text_data_json = json.loads(text_data)

        PrivateMessage.objects.create(author = User.objects.get(id=text_data_json['user']), 
                               text = text_data_json['text'],  
                               privateRoom = PrivateRoom.objects.get(id = text_data_json['privateRoom']))

        async_to_sync(self.channel_layer.group_send)(
            "chat",
            {
                "type": "chat.message",
                "text": text_data,
            },
        )

    def chat_message(self, event):
        self.send(text_data=event["text"])