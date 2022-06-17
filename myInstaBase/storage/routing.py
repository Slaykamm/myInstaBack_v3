from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
   # re_path(r'userAPI', consumers.ChatConsumer.as_asgi()),
    re_path(r'api/prvatemessages/', consumers.ChatConsumer.as_asgi()),

    ]