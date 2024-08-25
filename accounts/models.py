# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        expiration_time = timezone.now() - timezone.timedelta(minutes=10)
        return self.created_at >= expiration_time
