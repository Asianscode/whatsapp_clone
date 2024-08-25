# contact/urls.py
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('api/', views.add_contact, name='add_contact'),
    path('api/', views.remove_contact, name='remove_contact'),  # Endpoint to remove an existing contact
    path('api/', views.list_contacts, name='list_contacts'),  # Endpoint to list contacts with pagination and search
    path('api/', include(router.urls)),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
