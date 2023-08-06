import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pony_indice.tests.testproject.settings")
application = get_wsgi_application()
