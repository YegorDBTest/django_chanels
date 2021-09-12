from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('send_message/<str:room_name>/<str:message>/', views.send_chat_message, name='send_chat_message'),
]
