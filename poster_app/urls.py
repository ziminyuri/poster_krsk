from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path

from .views import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth_user", views.auth_user, name="auth_user"),
    path("profile", views.profile, name="profile"),
    path("events", views.events, name="events"),
    path("event/<int:event_id>", views.event_detail, name="event_detail"),
    path("booking", views.booking, name="booking"),
    path("concert", views.concert, name="concert"),
    path(
        "concert/<int:event_id>",
        views.concert_update_detail,
        name="concert_update_detail",
    ),
    path("conference", views.conference, name="conference"),
    path(
        "conference/<int:event_id>",
        views.conference_update_detail,
        name="conference_update_detail",
    ),
    path("exhibition", views.exhibition, name="exhibition"),
    path(
        "exhibition/<int:event_id>",
        views.exhibition_update_detail,
        name="exhibition_update_detail",
    ),
    path("theater", views.theater, name="theater"),
    path(
        "theater/<int:event_id>",
        views.theater_update_detail,
        name="theater_update_detail",
    ),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
