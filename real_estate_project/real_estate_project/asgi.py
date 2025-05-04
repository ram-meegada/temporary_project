import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import Tensor_App.routers
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'real_estate_project.settings')

wsgi_application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": wsgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack
            (
                URLRouter(
                    Tensor_App.routers.websocket_urlpatterns
                )
            ))
    }
)
