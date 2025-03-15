from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_django_app.settings')

application = get_asgi_application()