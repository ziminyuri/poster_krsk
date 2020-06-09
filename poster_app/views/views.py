import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from poster_app.models import *
from poster_app.views.logics import update_event, add_event, get_username, is_admin, admin_update
from django.contrib.auth import logout

import datetime


def index(request):
    title = 'События'
    events = Event.objects.all().filter(id_event_status__name='Опубликовано')

    name = get_username(request)
    flag_admin = is_admin(request)

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,
                                           'admin': flag_admin}
    )


def index_detail(request, event_id: int):
    event = get_object_or_404(Event, ID_event=event_id)

    if event.ID_type_event.name == "Выставка":
        return redirect("index_exhibition_detail", event_id=event_id)

    elif event.ID_type_event.name == "Концерт":
        return redirect("index_concert_detail", event_id=event_id)

    elif event.ID_type_event.name == "Конференция":
        return redirect("index_conference_detail", event_id=event_id)

    elif event.ID_type_event.name == "Театр":
        return redirect("index_theater_detail", event_id=event_id)


def booking(request, event_id: int):
    if request.POST:
        booking_place = request.POST["booking_place_input"]
        places_str = booking_place.split('Выбрано место: Ряд №')[1:]
        for place in places_str:
            row = place.split(' Место №')[0]
            pl = place.split(' Место №')[1]
            s = Setting.objects.all()[0]

            now = datetime.datetime.now()
            user = get_object_or_404(UserProfile, user=request.user)



        return HttpResponse(json.dumps("Бронирование прошло успешно"), content_type="application/json")

    else:
        name = get_username(request)
        rows = []
        for i in range(1, 11):
            rows.append(i)

        places = []
        for i in range(1, 21):
            places.append(i)

        event = get_object_or_404(Event, ID_event=event_id)

        return render(request, "poster_app/booking.html", {'name': name, 'rows': rows, 'places': places, 'event': event})


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


def index_concert_detail(request, event_id: int):
    name = get_username(request)
    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/index_detail/concert.html", {"event": event, 'name': name})


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


def index_conference_detail(request, event_id: int):
    name = get_username(request)
    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/index_detail/conference.html", {"event": event, 'name': name})


def index_exhibition(request):
    title = 'Выставки'
    name = get_username(request)
    flag_admin = is_admin(request)

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Выставка')

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name, 'admin': flag_admin}
    )


def index_exhibition_detail(request, event_id: int):
    name = get_username(request)
    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/index_detail/exhibition.html", {"event": event, 'name': name})


def index_theater(request):
    title = 'Театр'
    name = get_username(request)
    flag_admin = is_admin(request)

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name=title)

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name, 'admin': flag_admin}
    )


def index_theater_detail(request, event_id: int):
    name = get_username(request)
    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/index_detail/theater.html", {"event": event, 'name': name})


def auth_user(request):
    if request.is_ajax() and request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
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
                auth.login(request, user)
                return HttpResponse(json.dumps("Success"), content_type="application/json")

    return render(request, "poster_app/registration.html", {'name': name})


def search(request):
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

    name = get_username(request)
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
            # description_len: str = str(2000 - len(event.description))

            if event_type == "Выставка":
                exhibition_types = TypeExhibition.objects.all()
                return render(
                    request,
                    "poster_app/event/exhibition/update.html",
                    {"exhibition_types": exhibition_types, "event": event,
                     'name': name},
                )

            elif event_type == "Театр":
                return render(
                    request, "poster_app/event/theater/update.html", {"event": event,
                                                                      'name': name}
                )

            elif event_type == "Концерт":
                return render(
                    request, "poster_app/event/concert/update.html", {"event": event,
                                                                      'name': name
                                                                      }
                )

            elif event_type == "Конференция":
                return render(
                    request, "poster_app/event/conference/update.html", {"event": event,
                                                                         'name': name}
                )

        elif data["_method"] == "DELETE":
            event = data["event"]
            event_obj = Event.objects.get(ID_event=event)
            event_obj.delete()
            return redirect("events")

    userprofile = UserProfile.objects.all().filter(user=request.user).first()
    events_list = Event.objects.all().filter(ID_user_profile=userprofile)
    event_types = TypeEvent.objects.all()

    if events_list:
        flag_event = True
    else:
        flag_event = False

    return render(
        request,
        "poster_app/user/events.html",
        {"events": events_list, "event_types": event_types, 'name': name, 'flag_event': flag_event})


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
def booking_user(request):
    name = get_username(request)
    return render(request, "poster_app/user/my_booking.html", {'name': name})


@login_required
def booking_list(request, event_id: int):
    name = get_username(request)
    return render(request, "poster_app/user/booking_list.html", {'name': name})


@login_required
def concert(request):
    name = get_username(request)
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Концерт')

            return redirect("events")

    return render(request, "poster_app/event/concert/add.html", {'name': name})


@login_required
def concert_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Концерт')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/concert/detail.html", {"event": event, 'name': name})


@login_required
def conference(request):
    name = get_username(request)
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Конференция')
            return redirect("events")

    return render(request, "poster_app/event/conference/add.html", {'name': name})


@login_required
def conference_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Конференция')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/conference/detail.html", {"event": event, 'name': name})


@login_required
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


@login_required
def exhibition_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Выставка')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/exhibition/detail.html", {"event": event, 'name': name})


@login_required
def theater(request):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Театр')
            return redirect("events")

    return render(request, "poster_app/event/theater/add.html", {'name': name})


@login_required
def theater_update_detail(request, event_id: int):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            update_event(request, data, event_id, 'Театр')
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/theater/detail.html", {"event": event, 'name': name})


@user_passes_test(lambda u: u.is_superuser)
def moderation(request):
    name = get_username(request)
    events = Event.objects.all().filter(id_event_status__name='Ожидает проверки')
    return render(request, "poster_app/administrator/moderation.html", {"events": events, 'name': name})


@user_passes_test(lambda u: u.is_superuser)
def published(request):
    name = get_username(request)
    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    return render(request, "poster_app/administrator/published.html", {"events": events, 'name': name})


@user_passes_test(lambda u: u.is_superuser)
def rejected(request):
    name = get_username(request)
    events = Event.objects.all().filter(id_event_status__name='Отклонено')
    return render(request, "poster_app/administrator/rejected.html", {"events": events, 'name': name})


@user_passes_test(lambda u: u.is_superuser)
def archive(request):
    name = get_username(request)
    events = Event.objects.all().filter(id_event_status__name='Архив')
    return render(request, "poster_app/administrator/archive.html", {"events": events, 'name': name})


@user_passes_test(lambda u: u.is_superuser)
def admin_detail(request, event_id: int):
    event = get_object_or_404(Event, ID_event=event_id)

    if event.ID_type_event.name == "Выставка":
        return redirect("admin_exhibition_detail", event_id=event_id)

    elif event.ID_type_event.name == "Концерт":
        return redirect("admin_concert_detail", event_id=event_id)

    elif event.ID_type_event.name == "Конференция":
        return redirect("admin_conference_detail", event_id=event_id)

    elif event.ID_type_event.name == "Театр":
        return redirect("admin_theater_detail", event_id=event_id)


@user_passes_test(lambda u: u.is_superuser)
def admin_concert_detail(request, event_id: int):
    if admin_update(request, event_id):
        return redirect('moderation')
    else:
        name = get_username(request)
        event = get_object_or_404(Event, ID_event=event_id)
        return render(request, "poster_app/administrator/detail/concert.html", {"event": event, 'name': name})


@user_passes_test(lambda u: u.is_superuser)
def admin_conference_detail(request, event_id: int):
    if admin_update(request, event_id):
        return redirect('moderation')
    else:
        name = get_username(request)
        event = get_object_or_404(Event, ID_event=event_id)
        return render(request, "poster_app/administrator/detail/conference.html", {"event": event, 'name': name})


@user_passes_test(lambda u: u.is_superuser)
def admin_exhibition_detail(request, event_id: int):
    flag_redirect = admin_update(request, event_id)
    if flag_redirect is False:
        name = get_username(request)
        event = get_object_or_404(Event, ID_event=event_id)
        return render(request, "poster_app/administrator/detail/exhibition.html", {"event": event, 'name': name})
    elif flag_redirect == "Ожидает проверки":
        return redirect('moderation')
    elif flag_redirect == "Опубликовано":
        return redirect('published')
    elif flag_redirect == "Отклонено":
        return redirect('rejected')
    else:
        return redirect('archive')


@user_passes_test(lambda u: u.is_superuser)
def admin_theater_detail(request, event_id: int):
    flag_redirect = admin_update(request, event_id)
    if flag_redirect is False:
        name = get_username(request)
        event = get_object_or_404(Event, ID_event=event_id)
        return render(request, "poster_app/administrator/detail/theater.html", {"event": event, 'name': name})
    elif flag_redirect == "Ожидает проверки":
        return redirect('moderation')
    elif flag_redirect == "Опубликовано":
        return redirect('published')
    elif flag_redirect == "Отклонено":
        return redirect('rejected')
    else:
        return redirect('archive')


@user_passes_test(lambda u: u.is_superuser)
def admin_concert_update(request, event_id: int):
    flag_redirect = admin_update(request, event_id)
    if flag_redirect is False:
        name = get_username(request)
        event = get_object_or_404(Event, ID_event=event_id)
        return render(request, "poster_app/administrator/update/concert_update.html", {"event": event, 'name': name})
    elif flag_redirect == "Ожидает проверки":
        return redirect('moderation')
    elif flag_redirect == "Опубликовано":
        return redirect('published')
    elif flag_redirect == "Отклонено":
        return redirect('rejected')
    else:
        return redirect('archive')


@user_passes_test(lambda u: u.is_superuser)
def admin_conference_update(request, event_id: int):
    flag_redirect = admin_update(request, event_id)
    if flag_redirect is False:
        name = get_username(request)
        event = get_object_or_404(Event, ID_event=event_id)
        return render(request, "poster_app/administrator/update/conference_update.html", {"event": event, 'name': name})
    elif flag_redirect == "Ожидает проверки":
        return redirect('moderation')
    elif flag_redirect == "Опубликовано":
        return redirect('published')
    elif flag_redirect == "Отклонено":
        return redirect('rejected')
    else:
        return redirect('archive')


@user_passes_test(lambda u: u.is_superuser)
def admin_events(request):
    name = get_username(request)

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            status = ['Опубликовано', 'Отклонено', 'Архив']
            event_type: str = data["event_type"]
            event_id: int = int(data["event"])
            event = get_object_or_404(Event, ID_event=event_id)

            if event_type == "Выставка":
                return render(request, "poster_app/administrator/update/exhibition_update.html",
                              {"event": event, 'name': name,
                               'status': status})

            elif event_type == "Театр":
                return render(request, "poster_app/administrator/update/exhibition_update.html", {"event": event,
                                                                                                  'name': name,
                                                                                                  'status': status})

            elif event_type == "Концерт":
                return render(request, "poster_app/administrator/update/concert_update.html",
                              {"event": event, 'name': name, 'status': status})

            elif event_type == "Конференция":
                return render(request, "poster_app/administrator/update/conference_update.html",
                              {"event": event, 'name': name, 'status': status})

        elif data["_method"] == "DELETE":
            event = data["event"]
            event_obj = Event.objects.get(ID_event=event)
            event = Event.objects.filter(ID_event=event).first()
            old_status = event.id_event_status.name
            event_obj.delete()

            if old_status == 'Ожидает проверки':
                return redirect("moderation")
            elif old_status == 'Опубликовано':
                return redirect('published')
            elif old_status == 'Архив':
                return redirect('archive')
            else:
                return redirect('rejected')
