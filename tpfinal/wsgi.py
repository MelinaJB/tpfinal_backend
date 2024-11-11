"""
WSGI config for tpfinal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tpfinal.settings')

application = get_wsgi_application()

# Esto asegura que el servidor use el puerto que Render asigna
port = os.getenv('PORT', '8000')  # Render asigna un puerto dinámico, se usa el 8000 por defecto
