from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from .models import Message, Media
from .serializers import MessageSerializer, MediaSerializer
import logging
from django.http import HttpResponseServerError, Http404, JsonResponse
from django.db import DatabaseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.http import require_POST

# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
def home(request):
    """
    Render the homepage for authenticated users.
    """
    try:
        return render(request, 'home.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {e}", exc_info=True)
        messages.error(request, "An unexpected error occurred while loading the home page. Please try again later.")
        return redirect('error_page')

@login_required
def chat(request):
    """
    Render the chat interface for authenticated users.
    """
    try:
        return render(request, 'chat/chat.html')
    except DatabaseError as e:
        logger.error(f"Database error rendering chat page: {e}", exc_info=True)
        messages.error(request, "A database error occurred while loading the chat page. Please try again later.")
        return redirect('error_page')
    except Exception as e:
        logger.error(f"Error rendering chat page: {e}", exc_info=True)
        messages.error(request, "An unexpected error occurred while loading the chat page. Please try again later.")
        return redirect('error_page')

@login_required
@require_POST
def load_chat(request):
    """
    Load the chat for the selected contact.
    """
    contact_id = request.POST.get('contact_id')
    if not contact_id:
        return JsonResponse({'status': 'error', 'message': 'No contact ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Fetch the messages for the selected contact
        messages = Message.objects.filter(sender=request.user, recipient_id=contact_id) | \
                   Message.objects.filter(sender_id=contact_id, recipient=request.user)
        messages = messages.order_by('timestamp')

        # Serialize the messages
        message_data = MessageSerializer(messages, many=True).data
        return JsonResponse({'status': 'success', 'messages': message_data})
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Messages not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error loading chat: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred while loading the chat.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def error_page(request):
    """
    Render a custom error page.
    """
    return render(request, 'error.html')

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def create(self, request, *args, **kwargs):
        """
        Override create method to handle sending messages.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error creating message: {e}", exc_info=True)
            return Response({"error": "An unexpected error occurred while sending the message."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        """
        Override list method to handle listing messages.
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing messages: {e}", exc_info=True)
            return Response({"error": "An unexpected error occurred while retrieving messages."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve method to handle retrieving a specific message.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            logger.error(f"Message not found: {kwargs.get('pk')}", exc_info=True)
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving message: {e}", exc_info=True)
            return Response({"error": "An unexpected error occurred while retrieving the message."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def upload_media(request):
    file = request.FILES.get('file')
    
    if not file:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    media = Media.objects.create(user=request.user, file=file)
    serializer = MediaSerializer(media)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@login_required
def upload_voice(request):
    file = request.FILES.get('file')
    
    if not file:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    media = Media.objects.create(user=request.user, file=file, media_type='voice')
    serializer = MediaSerializer(media)
    return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)