# mysite/asgi.py
import os
import django
# from decouple import config
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkherebackend.settings')
django.setup()

import chat.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

# import os
# import django
# from decouple import config
# from channels.routing import get_default_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
# django.setup()
# application = get_default_application()