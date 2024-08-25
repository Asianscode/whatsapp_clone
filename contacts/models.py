# contact/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')
            )
        ]
    )
    contact_email = models.EmailField(
        null=True, 
        blank=True,
        validators=[EmailValidator(message=_('Enter a valid email address.'))]
    )
    profile_picture = models.ImageField(
        upload_to='contact_pics/', 
        null=True, 
        blank=True,
        help_text=_('Upload a profile picture for the contact.')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return f'{self.name} - {self.phone_number} - {self.contact_email}'

    def save(self, *args, **kwargs):
        # Implement any custom save logic if needed (e.g., resizing images)
        super().save(*args, **kwargs)
