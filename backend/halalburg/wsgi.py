"""
WSGI config for HalalBurg Terminal Django backend.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halalburg.settings")
application = get_wsgi_application()
