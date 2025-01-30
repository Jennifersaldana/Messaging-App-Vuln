"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Set the Python Home for the virtual environment
sys.path.insert(0, '/home/clayton/LSU/CSC/IntroCyber/Project/Cyber-Project')
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'

# Point to the virtual environment Python
os.environ['PYTHONHOME'] = '/home/clayton/LSU/CSC/IntroCyber/Project/Cyber-Project/venv'

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()