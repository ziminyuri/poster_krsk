import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from poster_app.models import *
from poster_app.views.logics import update_event, add_event


def index(request):
    title = 'События'
    events = Event.objects.all().filter(id_event_status__name='Опубликовано')

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title}
    )


def index_concert(request):
    title = 'Концерты'

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Концерт')


    return render(
        request, "poster_app/index.html", {"events": events, 'title': title}
    )


def index_conference(request):
    title = 'Конференции'

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Конференция')

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title}
    )


def index_exhibition(request):
    title = 'Выставки'

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Выставка')

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title}
    )


def index_theater(request):
    title = 'Театр'

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name=title)

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title}
    )


def auth_user(request):
    if request.is_ajax() and request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponse(json.dumps("Sign in"), content_type="application/json")

        else:
            return HttpResponse(
                json.dumps("Error sign in"), content_type="application/json"
            )


def search(request):
    events = Event.objects.all()
    return render(
        request, "poster_app/search.html", {"events": events}
    )

@login_required
def profile(request):
    return render(request, "poster_app/user/profile.html")


@login_required
def events(request):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            event_type = data["event_type"]

            if event_type == "Выставка":
                return redirect("exhibition")
            elif event_type == "Театр":
                return redirect("theater")
            elif event_type == "Концерт":
                return redirect("concert")
            elif event_type == "Конференция":
                return redirect("conference")

        elif data["_method"] == "PUT":
            event_type: str = data["event_type"]
            event_id: int = int(data["event"])
            event = get_object_or_404(Event, ID_event=event_id)
            description_len: str = str(2000 - len(event.description))

            if event_type == "Выставка":
                exhibition_types = TypeExhibition.objects.all()
                return render(
                    request,
                    "poster_app/event/exhibition/update.html",
                    {"exhibition_types": exhibition_types, "event": event, "description_len": description_len},
                )

            elif event_type == "Театр":
                return render(
                    request, "poster_app/event/theater/update.html", {"event": event,
                                                                      "description_len": description_len}
                )

            elif event_type == "Концерт":
                return render(
                    request, "poster_app/event/concert/update.html", {"event": event,  "description_len": description_len}
                )

            elif event_type == "Конференция":
                return render(
                    request, "poster_app/event/conference/update.html", {"event": event,  "description_len": description_len}
                )

        elif data["_method"] == "DELETE":
            event = data["event"]
            event_obj = Event.objects.get(ID_event=event)
            event_obj.delete()
            return redirect("events")

    events_list = Event.objects.all()
    event_types = TypeEvent.objects.all()
    return render(
        request,
        "poster_app/user/events.html",
        {"events": events_list, "event_types": event_types},
    )


def event_detail(request, event_id: int):
    event = get_object_or_404(Event, ID_event=event_id)

    if event.ID_type_event.name == "Выставка":
        return redirect("exhibition_update_detail", event_id=event_id)

    elif event.ID_type_event.name == "Концерт":
        return redirect("concert_update_detail", event_id=event_id)

    elif event.ID_type_event.name == "Конференция":
        return redirect("conference_update_detail", event_id=event_id)

    elif event.ID_type_event.name == "Театр":
        return redirect("theater_update_detail", event_id=event_id)


@login_required
def booking(request):
    return render(request, "poster_app/user/booking.html")


def concert(request):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Концерт')

            return redirect("events")

    return render(request, "poster_app/event/concert/add.html")


def concert_update_detail(request, event_id: int):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Концерт')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/concert/detail.html", {"event": event})


def conference(request):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Конференция')
            return redirect("events")

    return render(request, "poster_app/event/conference/add.html")


def conference_update_detail(request, event_id: int):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Конференция')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/conference/detail.html", {"event": event})


def exhibition(request):

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Выставка')
            return redirect("events")

    exhibition_types = TypeExhibition.objects.all()
    return render(
        request,
        "poster_app/event/exhibition/add.html",
        {"exhibition_types": exhibition_types},
    )


def exhibition_update_detail(request, event_id: int):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Выставка')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/exhibition/detail.html", {"event": event})


def theater(request):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Театр')
            return redirect("events")

    return render(request, "poster_app/event/theater/add.html")


def theater_update_detail(request, event_id: int):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Театр')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/theater/detail.html", {"event": event})
