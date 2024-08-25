# chat/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import MessageViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('error/', views.error_page, name='error_page'),
     path('upload-media/', views.upload_media, name='upload_media'),
     path('upload-voice/', views.upload_voice, name='upload_voice'),
    path('api/', include(router.urls)),
]
