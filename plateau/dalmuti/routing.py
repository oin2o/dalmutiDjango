from django.urls import re_path
from django.conf.urls import url

from . import consumers


websocket_urlpatterns = [
    url(r'dalmuti/(?P<gamename>\w+)/(?P<username>\w+)', consumers.dalmuti_consumer),
    url(r'dalmutip/(?P<gamename>\w+)/(?P<username>\w+)', consumers.dalmuti_consumer),
    url(r'dalmutid/(?P<gamename>\w+)/(?P<username>\w+)', consumers.dalmuti_consumer),
    url(r'liar/(?P<gamename>\w+)/(?P<username>\w+)', consumers.dalmuti_consumer),
]
