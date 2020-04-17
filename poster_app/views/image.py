from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.shortcuts import get_object_or_404
from poster_app.models import Event


def image_to_db(request, user, event_id=None, f_update=False) -> str:
    try:
        uploaded_img = request.FILES["upload_image"]
        fs = FileSystemStorage()
        save_root: str = settings.MEDIA_ROOT + "/" + user.user.username + "/" + uploaded_img.name
        fs.save(save_root, uploaded_img)

        basewidth: int = 223

        pillow_img: Image = Image.open(save_root)
        wpercent: float = (basewidth / float(pillow_img.size[0]))
        hsize: int = int((float(pillow_img.size[1]) * float(wpercent)))
        pillow_img: Image = pillow_img.resize((basewidth, hsize), Image.ANTIALIAS)
        pillow_img.save(save_root)

        img_path_db: str = settings.MEDIA_URL + user.user.username + "/" + uploaded_img.name

    except:
        if f_update:
            event = get_object_or_404(Event, ID_event=event_id)
            img = event.img
            img_path_db = img.name

        else:
            img_path_db = settings.MEDIA_URL + "defualt.jpg"

    return img_path_db
