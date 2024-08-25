# chat/middleware.py
import logging
from sqlite3 import DatabaseError
from django.http import Http404, HttpResponseServerError
from django.shortcuts import render

logger = logging.getLogger(__name__)

class CustomErrorMiddleware:
    """
    Middleware to handle exceptions and provide a custom error response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Exception caught by middleware: {e}", exc_info=True)
            return self.handle_exception(request, e)

    def handle_exception(self, request, exception):
        if isinstance(exception, Http404):
            return render(request, '404.html', status=404)
        if isinstance(exception, DatabaseError):
            return HttpResponseServerError("A database error occurred. Please try again later.")
        return render(request, '500.html', status=500)
