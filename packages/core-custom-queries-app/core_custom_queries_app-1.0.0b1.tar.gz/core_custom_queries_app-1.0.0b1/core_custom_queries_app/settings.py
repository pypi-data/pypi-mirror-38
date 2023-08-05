from django.conf import settings

if not settings.configured:
    settings.configure()

REDIS_HOST = getattr(settings, 'REDIS_HOST', "127.0.0.1")
REDIS_PORT = getattr(settings, 'REDIS_PORT', 6379)
