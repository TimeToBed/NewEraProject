# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.core.asgi import get_asgi_application
from . import consumers

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/path/in/your/app/", consumers.YourConsumer.as_asgi()),
    ]),
})