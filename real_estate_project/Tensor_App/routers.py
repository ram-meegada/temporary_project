from django.urls import path
from . import consumers
from .consumers import *

websocket_urlpatterns = [
    path('run/terraform/', BasicSyncConsumer.as_asgi()),
    path('details/', DetailsConsumer.as_asgi()),

]