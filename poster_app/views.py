from django.shortcuts import render, redirect
from .models import *
from django.contrib import auth
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests


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
            return HttpResponse(json.dumps("Sign in"), content_type='application/json')

        else:
            return HttpResponse(json.dumps("Error sign in"), content_type='application/json')

    #  event_exhibitions = Event.objects.all().filter(ID_type_event=1)
    # return render(request, 'poster_app/index.html', {'events_exhibitions': event_exhibitions})


@login_required
def profile(request):
    return render(request, 'poster_app/user/profile.html')


@login_required
def events(request):
    if request.method == 'POST':
        data = request.POST

        event_type = data['event_type']

        if event_type == "Выставка":
            return redirect('exhibition_add')
        elif event_type == 'Театр':
            return redirect('theater')
        elif event_type == "Концерт":
            return redirect('concert')
        elif event_type == "Конференция":
            return redirect('conference')

    events_list = Event.objects.all()
    event_types = TypeEvent.objects.all()
    return render(request, 'poster_app/user/events.html', {'events': events_list,
                                                           'event_types': event_types
                                                           })


@login_required
def booking(request):
    return render(request, 'poster_app/user/booking.html')


def concert(request):
    print('концерты')
    return render(request, 'poster_app/event/concert/detail.html')


def conference(request):
    print('конференция')
    return render(request, 'poster_app/event/conference/detail.html')


def exhibition(request):
    print('Выставка')
    return render(request, 'poster_app/event/exhibition/detail.html')


def exhibition_add(request):
    return render(request, 'poster_app/event/exhibition/add.html')



def theater(request):
    print('Театр')
    return render(request, 'poster_app/event/theater/detail.html')
