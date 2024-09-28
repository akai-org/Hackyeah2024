
from django.urls import re_path
from . import chatsocket

websocket_urlpatterns = [
    re_path(r'ws/chat/$', chatsocket.ChatSockets.as_asgi()),
]
