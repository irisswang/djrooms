from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/DJRoom/(?P<room_name>\w+)/(?P<user_dj>\w+)/$', consumers.ChatConsumer),
]