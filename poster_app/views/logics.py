from django.shortcuts import get_object_or_404
from poster_app.models import UserProfile, EventStatus, Event, TypeEvent, TypeExhibition, Ticket, Setting, Booking,\
    StatusBooking, TypeTicket
from poster_app.views.image import image_to_db
from django.shortcuts import redirect

import datetime


def add_event(request, data, type):
    type_event = get_object_or_404(TypeEvent, name=type)
    id_type_ticket = data['ticket_type']
    type_ticket = get_object_or_404(TypeTicket, id_type_ticket=id_type_ticket)
    name = data["name"]
    description = data["description"]
    address = data["address"]
    time_begin = data["time_begin"]

    if type == 'Концерт' or type == 'Театр':
        date = data["date"]

    elif type == 'Конференция':
        date_begin = data["date_begin"]
        date_end = data["date_end"]
        time_end = data["time_end"]

    elif type == 'Выставка':
        exhibition_type = get_object_or_404(
            TypeExhibition, id_type_exhibition=data["exhibition_type"]
        )
        time_end = data["time_end"]

        if exhibition_type.name == 'временная экспозиция':
            date_begin = data["date_begin"]
            date_end = data["date_end"]


    user = get_object_or_404(UserProfile, user=request.user)
    img_path_db = image_to_db(request, user)

    status = get_object_or_404(
        EventStatus, name='Ожидает проверки'
    )

    try:
        is_free = bool(data['123'])
    except:
        is_free = False

    if is_free is True:
        price = 0
    else:
        price = data["price"]

    if type == 'Концерт' or type == 'Театр':
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
            isfree=is_free,
            id_event_status=status,
            ID_type_ticket=type_ticket
        )

    elif type == 'Конференция':
        Event.objects.create(
            name=name,
            address=address,
            description=description,
            time_begin=time_begin,
            data_begin=date_begin,
            ticket_price=price,
            ID_type_event=type_event,
            ID_user_profile=user,
            img=img_path_db,
            isfree=is_free,
            id_event_status=status,
            data_end=date_end,
            time_end=time_end,
            ID_type_ticket=type_ticket
        )

    elif type == 'Выставка':
        if exhibition_type.name == 'временная экспозиция':
            Event.objects.create(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                ticket_price=price,
                ID_type_event=type_event,
                ID_user_profile=user,
                img=img_path_db,
                isfree=is_free,
                id_event_status=status,
                time_end=time_end,
                id_type_exhibition=exhibition_type,
                data_begin=date_begin,
                data_end=date_end,
                ID_type_ticket=type_ticket
            )

        else:
            Event.objects.create(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                ticket_price=price,
                ID_type_event=type_event,
                ID_user_profile=user,
                img=img_path_db,
                isfree=is_free,
                id_event_status=status,
                time_end=time_end,
                id_type_exhibition=exhibition_type,
                ID_type_ticket=type_ticket
            )


def update_event(request, data, event_id, type):
    name = data["name"]
    description = data["description"]
    address = data["address"]
    time_begin = data["time_begin"]

    if type == 'Концерт' or type == 'Театр':
        date = data["date"]
    elif type == 'Конференция':
        time_end = data["time_end"]
        date_begin = data["date_begin"]
        date_end = data["date_end"]
    elif type == 'Выставка':
        exhibition_type = get_object_or_404(
            TypeExhibition, id_type_exhibition=data["exhibition_type"]
        )

        f_exhibition_type_temp = 0
        if exhibition_type.name == 'временная экспозиция':
            date_begin = data["date_begin"]
            date_end = data["date_end"]
            f_exhibition_type_temp = 1

        time_end = data["time_end"]

    user = get_object_or_404(UserProfile, user=request.user)
    img_path_db = image_to_db(request, user, event_id=event_id, f_update=True)

    status = get_object_or_404(
        EventStatus, name='Ожидает проверки'
    )

    try:
        is_free = bool(data['123'])
    except:
        is_free = False

    if is_free is True:
        price = 0
    else:
        price = data["price"]

    if type == 'Концерт' or type == 'Театр':
        Event.objects.filter(ID_event=event_id).update(
            name=name,
            description=description,
            address=address,
            time_begin=time_begin,
            data_begin=date,
            ticket_price=price,
            img=img_path_db,
            isfree=is_free,
            id_event_status=status
        )

    elif type == 'Конференция':
        Event.objects.filter(ID_event=event_id).update(
            name=name,
            address=address,
            description=description,
            time_begin=time_begin,
            data_begin=date_begin,
            ticket_price=price,
            ID_user_profile=user,
            img=img_path_db,
            isfree=is_free,
            id_event_status=status,
            data_end=date_end,
            time_end=time_end
        )

    elif type == 'Выставка':
        if f_exhibition_type_temp:
            Event.objects.filter(ID_event=event_id).update(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                ticket_price=price,
                ID_user_profile=user,
                img=img_path_db,
                isfree=is_free,
                id_event_status=status,
                time_end=time_end,
                id_type_exhibition=exhibition_type,
                data_begin=date_begin,
                data_end=date_end
            )

        else:
            Event.objects.filter(ID_event=event_id).update(
                name=name,
                address=address,
                description=description,
                time_begin=time_begin,
                ticket_price=price,
                ID_user_profile=user,
                img=img_path_db,
                isfree=is_free,
                id_event_status=status,
                time_end=time_end,
                id_type_exhibition=exhibition_type
            )


def get_username(request):
    if request.user.is_authenticated:
        userprofile = UserProfile.objects.all().filter(user=request.user).first()
        name = userprofile.name
    else:
        name = None

    return name


def is_admin(request) -> bool:
    if request.user.is_authenticated:
        if request.user.is_superuser:
            flag: bool = True
        else:
            flag: bool = False
    else:
        flag: bool = 0

    return flag


def admin_update(request, event_id):
    if request.method == "POST":
        data = request.POST

        if data["_method"] == "PUT":
            status = data["status"]
            status = get_object_or_404(EventStatus, name=status)
            event = Event.objects.filter(ID_event=event_id).first()
            old_status = event.id_event_status.name
            Event.objects.filter(ID_event=event_id).update(id_event_status=status)

            return old_status
    else:
        return False


def add_ticket_place(request, event_id) -> bool:
    try:
        booking_place = request.POST["booking_place_input"]
        places_str = booking_place.split('Выбрано место: Ряд №')[1:]
        for place in places_str:
            row = place.split(' Место №')[0]
            pl = place.split(' Место №')[1]
            s = Setting.objects.first()

            now = datetime.datetime.now()
            status_booking = get_object_or_404(StatusBooking, name="Забронировано")
            user = get_object_or_404(UserProfile, user=request.user)
            booking = Booking.objects.create(
                number=s.number_booking,
                date=now,
                ID_user_profile=user,
                id_status_booking=status_booking
            )
            Setting.objects.filter(id_setting=s.id_setting).update(
                number_booking=s.number_booking + 1)

            event = Event.objects.filter(ID_event=event_id).first()

            try:
                ticket_price = int(event.ticket_price)
            except:
                ticket_price = 0

            if ticket_price > 0:
                isfree = 0
            else:
                isfree = 1

            Ticket.objects.create(
                row=row,
                place=pl,
                id_booking=booking,
                ID_event=event,
                isfree=isfree,
                ticket_price=ticket_price,
                date=event.data_begin
            )
        return True
    except:
        return False


def add_ticket_entrance(request, event_id) -> bool:
    try:
        date = request.POST["date_ticket"]
        s = Setting.objects.first()
        now = datetime.datetime.now()
        user = get_object_or_404(UserProfile, user=request.user)
        status_booking = get_object_or_404(StatusBooking, name="Забронировано")
        booking = Booking.objects.create(
            number=s.number_booking,
            date=now,
            ID_user_profile=user,
            id_status_booking=status_booking

        )
        Setting.objects.filter(id_setting=s.id_setting).update(
            number_booking=s.number_booking + 1)

        event = Event.objects.filter(ID_event=event_id).first()

        try:
            ticket_price = int(event.ticket_price)
        except Exception as e:
            ticket_price = 0

        if ticket_price > 0:
            isfree = 0
        else:
            isfree = 1

        Ticket.objects.create(
            id_booking=booking,
            ID_event=event,
            isfree=isfree,
            ticket_price=ticket_price,
            date=date
        )
        return True
    except Exception as e:
        return False