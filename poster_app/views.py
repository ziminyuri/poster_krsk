from django.shortcuts import render
from .models import *


def index(request):
    event_exhibitions = Event.objects.all().filter(ID_type_event=1)
    return render(request, 'poster_app/index.html', {'events_exhibitions': event_exhibitions})


def auth_user(request):
    event_exhibitions = Event.objects.all().filter(ID_type_event=1)
    return render(request, 'poster_app/index.html', {'events_exhibitions': event_exhibitions})
