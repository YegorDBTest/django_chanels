import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from channels_auth_token_middlewares.middleware import (
    DRFAuthTokenMiddleware, SimpleJWTAuthTokenMiddleware,
)
from chat.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    # "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(DRFAuthTokenMiddleware(
    # "websocket": AuthMiddlewareStack(SimpleJWTAuthTokenMiddleware(
        URLRouter(websocket_urlpatterns)
    )),
})
