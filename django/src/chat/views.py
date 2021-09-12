from asgiref.sync import async_to_sync

from channels import layers

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def send_chat_message(request, room_name, message):
    channel_layer = layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_%s' % room_name,
        {
            'type': 'chat_message',
            'message': message
        }
    )
    return HttpResponse()
