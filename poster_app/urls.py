from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth_user', views.auth_user, name='auth_user'),

    path('profile', views.profile, name='profile'),
    path('events', views.events, name='events'),
    path('event/<int:event_id>', views.event_detail, name='event_detail'),
    path('booking', views.booking, name='booking'),

    path('concert', views.concert, name='concert'),
    path('concert_add', views.concert_add, name='concert_add'),
    path('concert/<int:id>', views.concert_update, name='concert_update'),

    path('conference', views.conference, name='conference'),
    path('conference_add', views.conference_add, name='conference_add'),
    path('conference/<int:id>', views.conference_update, name='conference_update'),

    path('exhibition', views.exhibition, name='exhibition'),
    path('exhibition/add', views.exhibition_add, name='exhibition_add'),
    path('exhibition/<int:event_id>', views.exhibition_update, name='exhibition_update'),
    path('exhibition/detail/<int:event_id>', views.exhibition_detail, name='exhibition_detail'),

    path('theater', views.theater, name='theater'),
    path('theater_add', views.theater_add, name='theater_add'),
    path('theater/<int:id>', views.theater_update, name='theater_update'),
]
