# chat/serializer.py
from rest_framework import serializers
from .models import Message, Media

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'contact', 'text', 'created_at', 'media']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'user', 'file', 'created_at']