from django.shortcuts import get_object_or_404
from poster_app.models import UserProfile, EventStatus, Event, TypeEvent, TypeExhibition
from poster_app.views.image import image_to_db


def add_event(request, data, type):
    type_event = get_object_or_404(TypeEvent, name=type)
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
            id_event_status=status
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
            time_end=time_end
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
                data_end=date_end
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
                id_type_exhibition=exhibition_type
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