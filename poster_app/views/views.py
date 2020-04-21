import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from poster_app.models import *
from poster_app.views.logics import update_event, add_event, get_username, is_admin
from django.contrib.auth import logout


def index(request):
    title = 'События'
    events = Event.objects.all().filter(id_event_status__name='Опубликовано')

    name = get_username(request)
    flag_admin = is_admin(request)

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,
                                           'admin': flag_admin}
    )


def index_concert(request):
    title = 'Концерты'
    name = get_username(request)
    flag_admin = is_admin(request)

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Концерт')

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,
                                           'admin': flag_admin}
    )


def index_conference(request):
    title = 'Конференции'
    name = get_username(request)
    flag_admin = is_admin(request)

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Конференция')

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,
                                           'admin': flag_admin}
    )


def index_exhibition(request):
    title = 'Выставки'
    name = get_username(request)
    flag_admin = is_admin(request)

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Выставка')

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,'admin': flag_admin}
    )


def index_theater(request):
    title = 'Театр'
    name = get_username(request)
    flag_admin = is_admin(request)

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name=title)

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,'admin': flag_admin}
    )


def auth_user(request):
    if request.is_ajax() and request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return HttpResponse(json.dumps("Sign in superuser"), content_type="application/json")

        else:
            return HttpResponse(
                json.dumps("Error sign in"), content_type="application/json"
            )


def logout_view(request):
    logout(request)
    return redirect('index')


def registration(request):
    name = get_username(request)

    if request.is_ajax():
        if request.POST:
            name = request.POST["name"]
            surname = request.POST["surname"]
            login = request.POST["login"]
            password = request.POST["password"]
            password_repeat = request.POST["password_repeat"]
            email = request.POST["email"]
            phone = request.POST["phone"]

            if password != password_repeat:
                return HttpResponse(json.dumps("Пароли не совпадают"), content_type="application/json")

            user = User.objects.all().filter(username=login).first()
            if user:
                return HttpResponse(json.dumps("Логин занят. Попробуйте другой"), content_type="application/json")

            else:
                print('Надо создать пользователя')
                User.objects.create_user(login, email, password)
                user = auth.authenticate(username=login, password=password)
                UserProfile.objects.create(
                    user=user,
                    name=name,
                    surname=surname,
                    email=email,
                    phone=phone,
                )

                return HttpResponse(json.dumps("Success"), content_type="application/json")

    return render(request, "poster_app/registration.html", {'name': name})


def search(request):
    name = get_username(request)
    flag_admin = is_admin(request)

    flag_name = 0
    flag_description = 0

    name_events = []
    description_events = []

    if request.method == "POST":
        query_search = request.POST['search']
        query_search = query_search.lower()
        events = Event.objects.all()

        for event in events:
            name = event.name.lower()
            f = name.find(query_search)
            if f != -1:
                name_events.append(event)
                flag_name = 1

        for event in events:
            description = event.description.lower()
            f = description.find(query_search)
            if f != -1:
                description_events.append(event)
                flag_description = 1

    return render(
        request, "poster_app/search.html", {"name_events": name_events, 'description_events': description_events,
                                            'flag_name': flag_name, 'flag_description': flag_description,
                                            'name': name, 'admin': flag_admin}
    )

@login_required
def profile(request):
    name = get_username(request)
    return render(request, "poster_app/user/profile.html", {'name': name})


@login_required
def events(request):
    name = get_username(request)

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
                    {"exhibition_types": exhibition_types, "event": event, "description_len": description_len,
                     'name': name},
                )

            elif event_type == "Театр":
                return render(
                    request, "poster_app/event/theater/update.html", {"event": event,
                                                                      "description_len": description_len,
                                                                      'name': name}
                )

            elif event_type == "Концерт":
                return render(
                    request, "poster_app/event/concert/update.html", {"event": event,
                                                                      "description_len": description_len,
                                                                      'name': name
                                                                      }
                )

            elif event_type == "Конференция":
                return render(
                    request, "poster_app/event/conference/update.html", {"event": event,
                                                                         "description_len": description_len,
                                                                         'name': name}
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
        {"events": events_list, "event_types": event_types, 'name': name},
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
    name = get_username(request)
    return render(request, "poster_app/user/booking.html", {'name': name})


def concert(request):
    name = get_username(request)
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Концерт')

            return redirect("events")

    return render(request, "poster_app/event/concert/add.html", {'name': name})


def concert_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Концерт')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/concert/detail.html", {"event": event, 'name': name})


def conference(request):
    name = get_username(request)
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Конференция')
            return redirect("events")

    return render(request, "poster_app/event/conference/add.html", {'name': name})


def conference_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Конференция')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/conference/detail.html", {"event": event, 'name': name})


def exhibition(request):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Выставка')
            return redirect("events")

    exhibition_types = TypeExhibition.objects.all()
    return render(
        request,
        "poster_app/event/exhibition/add.html",
        {"exhibition_types": exhibition_types, 'name': name},
    )


def exhibition_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Выставка')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/exhibition/detail.html", {"event": event, 'name': name})


def theater(request):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Театр')
            return redirect("events")

    return render(request, "poster_app/event/theater/add.html", {'name': name})


def theater_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Театр')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/theater/detail.html", {"event": event, 'name': name})


def moderation(request):
    name = get_username(request)
    events = Event.objects.all()
    return render(request, "poster_app/administrator/moderation.html", {"events": events, 'name': name})