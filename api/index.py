"""
Vercel serverless function handler for Django application.

This handler wraps Django WSGI application to work with Vercel's serverless functions.
Note: Vercel is not ideal for Django - consider Render or Railway instead.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django before importing
import django
django.setup()

# Import WSGI application
from config.wsgi import application as django_app

# Vercel expects a handler function
def handler(request):
    """
    Vercel serverless function handler.
    Converts Vercel request to Django-compatible format.
    """
    from django.test import RequestFactory
    from django.core.handlers.wsgi import WSGIRequest
    
    # Convert Vercel request to Django request
    factory = RequestFactory()
    
    # Get request data
    method = request.method if hasattr(request, 'method') else 'GET'
    path = request.path if hasattr(request, 'path') else '/'
    headers = dict(request.headers) if hasattr(request, 'headers') else {}
    body = request.body if hasattr(request, 'body') else b''
    
    # Create Django request
    django_request = factory.generic(
        method=method,
        path=path,
        data=body,
        content_type=headers.get('Content-Type', ''),
    )
    
    # Add headers to request
    for key, value in headers.items():
        django_request.META[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Get response from Django
    from django.http import HttpResponse
    response = django_app(django_request)
    
    return response
