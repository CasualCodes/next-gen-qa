"""
ASGI config for ngq_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
## Defaults
import os
from django.core.asgi import get_asgi_application
## Additional Configuration for Websockets
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from ngq_app.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ngq_project.settings")

# application = get_asgi_application()
## Application configuration to include websockets
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

# Running
## daphne -b 0.0.0.0 -p 8000 your_project_name.asgi:application