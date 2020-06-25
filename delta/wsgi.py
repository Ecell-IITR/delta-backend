"""
WSGI config for delta project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if os.environ.get('ENVIRONMENT') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delta.settings.deployment')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delta.settings.development')

application = get_wsgi_application()
