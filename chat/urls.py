# from django.urls import path

# from . import views

# urlpatterns = [
#     path("", views.index, name="chat"),
#     path("send/", views.send_message, name="send_message"),
# ]
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="chat"),
    path("translate/", views.translate_text, name="translate_text"),
]