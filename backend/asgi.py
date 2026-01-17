import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

try:
    django_asgi_app = get_asgi_application()
except Exception as e:
    import traceback

    traceback.print_exc()
    raise e
