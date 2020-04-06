from django.shortcuts import render
from .models import *
from django.contrib import auth
import json
from django.http import HttpResponse


def index(request):
    event_exhibitions = Event.objects.all().filter(ID_type_event=1)
    return render(request, 'poster_app/index.html', {'events_exhibitions': event_exhibitions})


def auth_user(request):
    if request.is_ajax() and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponse(json.dumps(user), content_type='application/json')

        else:
            return HttpResponse(json.dumps("Error sign in"), content_type='application/json')

    #  event_exhibitions = Event.objects.all().filter(ID_type_event=1)
    # return render(request, 'poster_app/index.html', {'events_exhibitions': event_exhibitions})
