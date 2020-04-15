import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from poster_app.models import *
from poster_app.views.image import image_to_db


def index(request):
    # event_exhibitions = Event.objects.all().filter(ID_type_event=1)
    event_exhibitions = Event.objects.all()

    return render(
        request, "poster_app/index.html", {"events_exhibitions": event_exhibitions}
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

            if event_type == "Выставка":
                exhibition_types = TypeExhibition.objects.all()
                return render(
                    request,
                    "poster_app/event/exhibition/update.html",
                    {"exhibition_types": exhibition_types, "event": event},
                )

            elif event_type == "Театр":
                description_len: str = str(len(event.description))
                return render(
                    request, "poster_app/event/theater/update.html", {"event": event,
                                                                      "description_len": description_len}
                )

            elif event_type == "Концерт":
                return render(
                    request, "poster_app/event/concert/update.html", {"event": event}
                )

            elif event_type == "Конференция":
                return render(
                    request, "poster_app/event/conference/update.html", {"event": event}
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
            type_event = get_object_or_404(TypeEvent, name="Концерт")
            name = data["name"]
            description = data["description"]
            address = data["address"]
            time_begin = data["time_begin"]
            date = data["date"]
            # isfree = data['free']
            price = data["price"]

            user = get_object_or_404(UserProfile, user=request.user)
            img_path_db = image_to_db(request, user)

            Event.objects.create(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                data_begin=date,
                ticket_price=price,
                ID_type_event=type_event,
                ID_user_profile=user,
                img=img_path_db,
            )

            return redirect("events")

    return render(request, "poster_app/event/concert/add.html")


def concert_update_detail(request, event_id: int):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            name = data["name"]
            description = data["description"]
            address = data["address"]
            time_begin = data["time_begin"]
            date = data["date"]
            # isfree = data['free']
            price = data["price"]

            user = get_object_or_404(UserProfile, user=request.user)
            img_path_db = image_to_db(request, user)

            Event.objects.filter(ID_event=event_id).update(
                name=name,
                description=description,
                address=address,
                time_begin=time_begin,
                data_begin=date,
                ticket_price=price,
                img=img_path_db,
            )

            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/concert/detail.html", {"event": event})


def conference(request):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            type_event = get_object_or_404(TypeEvent, name="Конференция")
            name = data["name"]
            description = data["description"]
            address = data["address"]
            date_begin = data["date_begin"]
            date_end = data["date_end"]
            time_begin = data["time_begin"]
            time_end = data["time_end"]
            # isfree = data['free']
            price = data["price"]

            user = get_object_or_404(UserProfile, user=request.user)
            img_path_db = image_to_db(request, user)

            Event.objects.create(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                time_end=time_end,
                ticket_price=price,
                ID_type_event=type_event,
                ID_user_profile=user,
                data_begin=date_begin,
                data_end=date_end,
                img=img_path_db,
            )

            return redirect("events")

    return render(request, "poster_app/event/conference/add.html")


def conference_update_detail(request, event_id: int):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            name = data["name"]
            description = data["description"]
            address = data["address"]
            time_begin = data["time_begin"]
            time_end = data["time_end"]
            # isfree = data['free']
            price = data["price"]
            date_begin = data["date_begin"]
            date_end = data["date_end"]

            user = get_object_or_404(UserProfile, user=request.user)
            img_path_db = image_to_db(request, user)

            Event.objects.filter(ID_event=event_id).update(
                name=name,
                description=description,
                address=address,
                time_begin=time_begin,
                time_end=time_end,
                ticket_price=price,
                data_begin=date_begin,
                data_end=date_end,
                img=img_path_db,
            )

            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/conference/detail.html", {"event": event})


def exhibition(request):

    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            type_event = get_object_or_404(TypeEvent, name="Выставка")
            name = data["name"]
            description = data["description"]
            address = data["address"]
            exhibition_type = get_object_or_404(
                TypeExhibition, id_type_exhibition=data["exhibition_type"]
            )
            time_begin = data["time_begin"]
            time_end = data["time_end"]
            # isfree = data['free']
            price = data["price"]
            user = get_object_or_404(UserProfile, user=request.user)

            img_path_db = image_to_db(request, user)
            Event.objects.create(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                time_end=time_end,
                ticket_price=price,
                id_type_exhibition=exhibition_type,
                ID_type_event=type_event,
                ID_user_profile=user,
                img=img_path_db,
            )

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
            name = data["name"]
            description = data["description"]
            address = data["address"]
            exhibition_type = get_object_or_404(
                TypeExhibition, id_type_exhibition=data["exhibition_type"]
            )
            time_begin = data["time_begin"]
            time_end = data["time_end"]
            # isfree = data['free']
            price = data["price"]
            user = get_object_or_404(UserProfile, user=request.user)
            img_path_db = image_to_db(request, user)

            Event.objects.filter(ID_event=event_id).update(
                name=name,
                description=description,
                address=address,
                id_type_exhibition=exhibition_type,
                time_begin=time_begin,
                time_end=time_end,
                ticket_price=price,
                img=img_path_db,
            )

            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/exhibition/detail.html", {"event": event})


def theater(request):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            type_event = get_object_or_404(TypeEvent, name="Театр")
            name = data["name"]
            description = data["description"]
            address = data["address"]
            time_begin = data["time_begin"]
            date = data["date"]
            # isfree = data['free']
            price = data["price"]

            user = get_object_or_404(UserProfile, user=request.user)
            img_path_db = image_to_db(request, user)

            Event.objects.create(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                data_begin=date,
                ticket_price=price,
                ID_type_event=type_event,
                ID_user_profile=user,
                img=img_path_db,
            )

            return redirect("events")

    return render(request, "poster_app/event/theater/add.html")


def theater_update_detail(request, event_id: int):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            name = data["name"]
            description = data["description"]
            address = data["address"]
            time_begin = data["time_begin"]
            date = data["date"]
            # isfree = data['free']
            price = data["price"]

            user = get_object_or_404(UserProfile, user=request.user)
            img_path_db = image_to_db(request, user)

            Event.objects.filter(ID_event=event_id).update(
                name=name,
                description=description,
                address=address,
                time_begin=time_begin,
                data_begin=date,
                ticket_price=price,
                img=img_path_db,
            )
            return redirect(events)

    event = get_object_or_404(Event, ID_event=event_id)
    return render(request, "poster_app/event/theater/detail.html", {"event": event})
