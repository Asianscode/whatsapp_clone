from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'contact_email', 'profile_picture', 'created_at', 'user']
        extra_kwargs = {
            'user': {'read_only': True},  # Ensure 'user' field is read-only
            'created_at': {'read_only': True},  # Ensure 'created_at' field is read-only
        }