import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat.middleware import DRFAuthTokenMiddleware
from chat.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(DRFAuthTokenMiddleware(
        URLRouter(websocket_urlpatterns)
    )),
})
