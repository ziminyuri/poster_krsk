import json
import os

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from poster_app.models import *
from poster_app.views.logics import update_event, add_event, get_username, is_admin, admin_update, add_ticket_place,\
    add_ticket_entrance
from django.contrib.auth import logout

from fpdf import FPDF


def index(request):
    title = 'События'
    events = Event.objects.all().filter(id_event_status__name='Опубликовано')

    name = get_username(request)
    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user=False
    flag_admin = is_admin(request)

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,
                                           'admin': flag_admin, 'user': user}
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
        type_ticket = request.POST["type_ticket"]

        if type_ticket == 'Входной':
            add_ticket_entrance(request, event_id)

        else:
            add_ticket_place(request, event_id)
        return redirect('booking_user')

    else:
        name = get_username(request)


        rows_label = []
        for i in range(1, 11):
            rows_label.append(i)

        rows = []
        for i in range(1, 11):
            places = []
            for i in range(1, 21):
                places.append(i)
            rows.append(places)

        event = get_object_or_404(Event, ID_event=event_id)

        tickets = Ticket.objects.filter(ID_event=event_id).all()

        for ticket in tickets:
            if ticket.id_booking.id_status_booking.name =='Забронировано' and ticket.ID_event.ID_type_ticket.name=='Место в зале':
                row = ticket.row
                place = ticket.place

                rows[row][place] = '-'
        return render(request, "poster_app/booking.html", {'name': name, 'event': event, 'places':rows})


# Отмена бронирования
def booking_disable(request):
    if request.POST:
        id_ticket = request.POST["id_ticket"]
        ticket = get_object_or_404(Ticket, id_ticket=id_ticket)
        id_booking = ticket.id_booking.id_booking
        status = get_object_or_404(StatusBooking, name="Отменено бронирование")
        Booking.objects.filter(id_booking=id_booking).update(id_status_booking=status)

    return redirect('booking_user')


def index_concert(request):
    title = 'Концерты'
    name = get_username(request)
    flag_admin = is_admin(request)

    events = Event.objects.all().filter(id_event_status__name='Опубликовано')
    events = events.filter(ID_type_event__name='Концерт')
    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user=False

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,
                                           'admin': flag_admin, 'user': user}
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

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user=False

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name,
                                           'admin': flag_admin, 'user': user}
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

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user=False

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name, 'admin': flag_admin,
                                           'user': user}
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

    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        user = False

    return render(
        request, "poster_app/index.html", {"events": events, 'title': title, 'name': name, 'admin': flag_admin,
                                           'user': user}
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
    user = get_object_or_404(UserProfile, user=request.user)
    return render(request, "poster_app/user/profile.html", {'name': name, 'user': user})


@login_required
def update_profile(request, profile_id: int):
    if request.POST:
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email1']
        phone = request.POST['phone']
        UserProfile.objects.filter(ID_user_profile=profile_id).update(
            name=name,
            surname=surname,
            email=email,
            phone=phone
        )

        return redirect('profile')

    name = get_username(request)
    user = get_object_or_404(UserProfile, user=request.user)
    return render(request, "poster_app/user/update_profile.html", {'name': name, 'user': user})


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
    user = get_object_or_404(UserProfile, user=request.user)
    b = Booking.objects.all()
    booking_list = Booking.objects.filter(ID_user_profile=user.ID_user_profile).all()
    tickets_list = []
    for booking in booking_list:
        tickets = Ticket.objects.filter(id_booking=booking.id_booking).all()
        for ticket in tickets:
            tickets_list.append(ticket)

    if tickets_list:
        flag_booking = True
    else:
        flag_booking = False

    return render(request, "poster_app/user/my_booking.html", {'name': name, 'tickets_list': tickets_list,
                                                               'flag_booking': flag_booking})


@login_required
def download_ticket_pdf(request):
    if request.method == 'POST':
        id_ticket = request.POST['id_ticket']
        ticket = get_object_or_404(Ticket, id_ticket=id_ticket)
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'poster_app/static/poster_app/font/DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(200, 10, txt="Билет", ln=1, align="C")
        pdf.cell(0, 5, '', ln=2)
        pdf.set_font('DejaVu', '', 12)
        name = ticket.ID_event.name
        pdf.cell(0, 5, 'Событие: ' + name, ln=1)
        pdf.cell(0, 5, '', ln=3)
        pdf.cell(0, 5, '', ln=3)

        pdf.cell(0, 5, 'Номер бронирования: ' + str(ticket.id_booking.number), ln=1)
        pdf.cell(0, 5, '', ln=2)
        pdf.cell(0, 5, 'Дата бронирования: ' + str(ticket.id_booking.date), ln=1)
        pdf.cell(0, 5, '', ln=3)
        pdf.cell(0, 5, '', ln=3)
        pdf.cell(0, 5, '', ln=2)
        pdf.cell(0, 5, 'Дата события: ' + str(ticket.date), ln=1)
        pdf.cell(0, 5, '', ln=3)

        if ticket.ID_event.ID_type_ticket.name == "Входной":
            pdf.cell(0, 5, 'Тип билета: ' + ticket.ID_event.ID_type_ticket.name, ln=1)
            pdf.cell(0, 5, '', ln=2)
        else:
            pdf.cell(0, 5, 'Ряд: ' + str(ticket.row), ln=1)
            pdf.cell(0, 5, '', ln=2)
            pdf.cell(0, 5, 'Место: ' + str(ticket.place), ln=1)
            pdf.cell(0, 5, '', ln=2)

        pdf.cell(0, 5, 'Адрес: ' + ticket.ID_event.address, ln=1)
        pdf.cell(0, 5, '', ln=2)

        if ticket.isfree == True:
            pdf.cell(0, 5, 'Стоимость: бесплатно', ln=1)
            pdf.cell(0, 5, '', ln=2)

        else:
            pdf.cell(0, 5, 'Стоимость: ' + ticket.ID_event.ticket_price + 'р', ln=1)
            pdf.cell(0, 5, '', ln=2)

        file_name = 'ticket.pdf'
        path_to_save_file = 'poster_app/static/poster_app/docs/ticket.pdf'
        pdf.output(path_to_save_file)
        data = open(path_to_save_file, "rb").read()
        response = HttpResponse(data, content_type='application;')
        response['Content-Length'] = os.path.getsize(path_to_save_file)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

        return response


@login_required
def booking_list(request, event_id: int):
    name = get_username(request)
    event = get_object_or_404(Event, ID_event=event_id)
    tickets = Ticket.objects.filter(ID_event=event).all()

    return render(request, "poster_app/user/booking_list.html", {'name': name, 'tickets': tickets, 'event': event})


@login_required
def booking_list_download(request, event_id: int):
    if request.method == 'POST':
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'poster_app/static/poster_app/font/DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(200, 10, txt="Список бронировния", ln=1, align="C")
        pdf.cell(0, 5, '', ln=2)
        event = get_object_or_404(Event, ID_event=event_id)
        pdf.cell(0, 5, 'Событие: ' + event.name, ln=1)
        pdf.cell(0, 5, '', ln=3)
        if event.isfree == True:
            pdf.cell(0, 5, 'Стоимость: бесплатно', ln=1)
        else:
            pdf.cell(0, 5, 'Стоимость: ' + event.ticket_price, ln=1)

        pdf.cell(0, 5, '', ln=3)

        row_height = pdf.font_size
        spacing = 2

        pdf.set_font('DejaVu', '', 9)
        pdf.cell(50, row_height * spacing, txt='Фамилия и имя', border=1)
        pdf.cell(37, row_height * spacing, txt='Номер бронирования', border=1)
        pdf.cell(40, row_height * spacing, txt='Дата бронирования', border=1)
        pdf.cell(10, row_height * spacing, txt='Ряд', border=1)
        pdf.cell(15, row_height * spacing, txt='Место', border=1)
        pdf.cell(45, row_height * spacing, txt='Статус бронировния', border=1)
        pdf.ln(row_height * spacing)

        tickets = Ticket.objects.filter(ID_event=event).all()

        pdf.set_font('DejaVu', '', 9)
        for ticket in tickets:
            pdf.cell(50, row_height * spacing,
                     txt=ticket.id_booking.ID_user_profile.surname + ' ' + ticket.id_booking.ID_user_profile.name,
                     border=1)
            pdf.cell(37, row_height * spacing, txt=str(ticket.id_booking.number), border=1)
            pdf.cell(40, row_height * spacing, txt=str(ticket.id_booking.date), border=1)
            if ticket.ID_event.ID_type_ticket.name == "Входной":
                pdf.cell(10, row_height * spacing, txt='-', border=1)
                pdf.cell(15, row_height * spacing, txt='-', border=1)
            else:
                pdf.cell(10, row_height * spacing, txt=str(ticket.row), border=1)
                pdf.cell(15, row_height * spacing, txt=str(ticket.place), border=1)
            pdf.cell(45, row_height * spacing, txt=ticket.id_booking.id_status_booking.name, border=1)
            pdf.ln(row_height * spacing)

        file_name = 'booking_list.pdf'
        path_to_save_file = 'poster_app/static/poster_app/docs/booking_list.pdf'
        pdf.output(path_to_save_file)
        data = open(path_to_save_file, "rb").read()
        response = HttpResponse(data, content_type='application;')
        response['Content-Length'] = os.path.getsize(path_to_save_file)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

        return response

@login_required
def concert(request):
    name = get_username(request)
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "POST":
            add_event(request, data, 'Концерт')

            return redirect("events")
    ticket_types = TypeTicket.objects.all()
    return render(request, "poster_app/event/concert/add.html", {'name': name, "ticket_types":ticket_types})


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

    ticket_types = TypeTicket.objects.all()
    return render(request, "poster_app/event/conference/add.html", {'name': name, 'ticket_types':ticket_types})


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
    ticket_types = TypeTicket.objects.all()
    return render(
        request,
        "poster_app/event/exhibition/add.html",
        {"exhibition_types": exhibition_types, 'name': name, "ticket_types": ticket_types},
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
    ticket_types = TypeTicket.objects.all()
    return render(request, "poster_app/event/theater/add.html", {'name': name, "ticket_types": ticket_types})


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
