import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import order.routing  # ✅ Make sure this matches your app name

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            order.routing.websocket_urlpatterns  # ✅ Matches your routing file
        )
    ),
})
