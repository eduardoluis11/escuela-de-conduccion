# This file contains the WSGI configuration required to serve up your
# Django app
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/proyecto_conduccion')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
import sys

# Add your project directory to the sys.path
settings_path = '/home/foxwolf11/foxwolf11.pythonanywhere.com'
sys.path.insert(0, settings_path)

# Set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto_conduccion.settings'

# Set the 'application' variable to the Django wsgi app
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
