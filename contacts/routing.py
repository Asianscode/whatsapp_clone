# project/routing.py
from django.urls import path, include
from chat import routing as chat_routing

websocket_urlpatterns = [
    path('ws/', include(chat_routing.websocket_urlpatterns)),  # Include chat WebSocket routing
]
