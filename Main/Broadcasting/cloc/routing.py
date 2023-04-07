from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/broadcast/", consumers.ChatConsumer.as_asgi()),
]