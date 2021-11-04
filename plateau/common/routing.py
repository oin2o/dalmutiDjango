from django.conf.urls import url

from . import consumers


websocket_urlpatterns = [
    url(r'dalmuti/(?P<gamename>\w+)/(?P<username>\w+)', consumers.common_consumer.as_asgi()),
    url(r'dalmutip/(?P<gamename>\w+)/(?P<username>\w+)', consumers.common_consumer.as_asgi()),
    url(r'dalmutid/(?P<gamename>\w+)/(?P<username>\w+)', consumers.common_consumer.as_asgi()),
    url(r'liar/(?P<gamename>\w+)/(?P<username>\w+)', consumers.common_consumer.as_asgi()),
    url(r'davinci/(?P<gamename>\w+)/(?P<username>\w+)', consumers.common_consumer.as_asgi()),
    url(r'dixit/(?P<gamename>\w+)/(?P<username>\w+)', consumers.common_consumer.as_asgi()),
]
