from django.urls import path
from channels.routing import URLRouter

from apps.bot.ws.urls import websocket_urlpatterns

websocket_urlpatterns = [
    path('websocket/', URLRouter(websocket_urlpatterns)),
]
