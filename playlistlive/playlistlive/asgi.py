"""
ASGI config for playlistlive project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import channels.asgi


from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playlistlive.settings')

application = get_asgi_application()
channel_layer = channels.asgi.get_channel_layer()
