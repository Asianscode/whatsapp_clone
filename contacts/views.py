from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer
from .forms import AddContactForm
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
@require_POST
def add_contact(request):
    form = AddContactForm(request.POST, request.FILES)  # Handle file uploads
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': 'Invalid form data.'}, status=status.HTTP_400_BAD_REQUEST)
    
    contact_email = form.cleaned_data['contact_email']
    if contact_email == request.user.email:
        return JsonResponse({'status': 'error', 'message': 'Cannot add yourself as a contact.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the contact email is already in the user's contacts
    existing_contact = Contact.objects.filter(user=request.user, contact_user__email=contact_email).exists()
    if existing_contact:
        return JsonResponse({'status': 'error', 'message': 'Contact already exists.'}, status=status.HTTP_409_CONFLICT)
    
    try:
        contact_user = User.objects.get(email=contact_email)
        contact, created = Contact.objects.get_or_create(user=request.user, contact_user=contact_user)
        
        if created:
            return JsonResponse({
                'status': 'success', 
                'contact': {
                    'id': contact.id, 
                    'name': contact.contact_user.username, 
                    'profile_picture': contact.profile_picture.url if contact.profile_picture else None
                }
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Contact already exists.'}, status=status.HTTP_409_CONFLICT)
    
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'invite', 
            'message': 'User not found. Would you like to invite them?',
            'invite_email': contact_email
        }, status=status.HTTP_404_NOT_FOUND)

@login_required
@require_POST
def remove_contact(request):
    contact_id = request.POST.get('id')
    if not contact_id:
        return JsonResponse({'status': 'error', 'message': 'No contact ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        contact = Contact.objects.get(id=contact_id, user=request.user)
        contact.delete()
        return JsonResponse({'status': 'success'})
    except Contact.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)

@login_required
@require_GET
def list_contacts(request):
    search_query = request.GET.get('q', '').strip()
    last_contact_id = request.GET.get('last_id', None)
    page_size = 10  # Number of contacts to load per scroll

    contacts = Contact.objects.filter(user=request.user)
    if search_query:
        contacts = contacts.filter(
            Q(contact_user__username__icontains=search_query) | 
            Q(contact_user__email__icontains=search_query)
        )

    if last_contact_id:
        contacts = contacts.filter(id__gt=last_contact_id)

    contacts = contacts.order_by('id')[:page_size]
    contact_list = [
        {
            'id': contact.id,
            'name': contact.contact_user.username,
            'profile_picture': contact.profile_picture.url if contact.profile_picture else None
        }
        for contact in contacts
    ]

    has_more = len(contact_list) == page_size
    return JsonResponse({'contacts': contact_list, 'has_more': has_more})

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def list(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '').strip()
        if search_query:
            self.queryset = self.queryset.filter(
                 Q(contact_user__username__icontains=search_query) | 
                Q(contact_user__email__icontains=search_query)
            )
        return super().list(request, *args, **kwargs)
