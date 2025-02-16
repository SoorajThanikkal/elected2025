import os
import django
import logging

logger = logging.getLogger('asgi')

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elected.settings')
    django.setup()

    from django.core.asgi import get_asgi_application
    from channels.routing import ProtocolTypeRouter, URLRouter
    from app.routing import wsPattern

    http_app = get_asgi_application()
    application = ProtocolTypeRouter({
        "http": http_app,
        "websocket": URLRouter(wsPattern),
    })

except Exception as e:
    logger.error(f"Error in ASGI configuration: {e}")
    raise