from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
import local.consumers

websocket_urlPattern = [
    path('ws/home/', local.consumers.Crawler),
    path('ws/search/', local.consumers.Searcher)
]

application = ProtocolTypeRouter(
    {
        'websocket': AuthMiddlewareStack(URLRouter(websocket_urlPattern))
    }
)
