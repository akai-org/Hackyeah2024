# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatsocket.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxHackYeah.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatsocket.routing.websocket_urlpatterns
        )
    ),
})
