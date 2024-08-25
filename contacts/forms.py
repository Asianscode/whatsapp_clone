# contact/forms.py
from django import forms
from .models import Contact

class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'contact_email', 'profile_picture']

    # Custom validation for phone_number
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Add any additional phone number validation logic here
            return phone_number
        raise forms.ValidationError('Phone number is required.')

    # Custom validation for contact_email
    def clean_contact_email(self):
        contact_email = self.cleaned_data.get('contact_email')
        if contact_email:
            # Add any additional email validation logic here
            return contact_email
        return None  # Allowing blank email addresses

    # Optional: Add custom validation for profile_picture
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Check file size, format, etc.
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Profile picture file size exceeds the 5MB limit.')
            return profile_picture
        return None
