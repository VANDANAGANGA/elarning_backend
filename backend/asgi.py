
# # asgi.py
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack



from accounts.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)
# import os

# def start_application():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
#     from django.core.asgi import get_asgi_application
#     return get_asgi_application()

# application = start_application()
