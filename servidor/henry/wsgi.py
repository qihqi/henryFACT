import sys
sys.path.append('/var/servidor/henry')
import os
os.environ["HOME"] = "/home/servidor/"
# This application object is used by the development server
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
