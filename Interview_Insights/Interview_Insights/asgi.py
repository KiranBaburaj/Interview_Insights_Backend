# asgi.py

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from chat.consumers import ChatConsumer
from channels.security.websocket import AllowedHostsOriginValidator
from chat.middleware import JwtAuthMiddlewareStack  # You'll need to create this

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Interview_Insights.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        JwtAuthMiddlewareStack(
            URLRouter([
                re_path(r"ws/chat/(?P<room_id>\w+)/$", ChatConsumer.as_asgi()),
            ])
        )
    ),
})