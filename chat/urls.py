# from django.conf.urls import include
from django.urls import path

from chat.views import make_message

app_name = 'chat'

urlpatterns = [
    path('send/', make_message, name="send_message"),
]
