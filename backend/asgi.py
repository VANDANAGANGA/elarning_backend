
# # asgi.py
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack



# from accounts.routing import websocket_urlpatterns

# application = ProtocolTypeRouter(
#     {
#         'http': get_asgi_application(),
#         'websocket': AuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         ),
#     }
# )
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from accounts.routing import websocket_urlpatterns

def start_application():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    return get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': start_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)

