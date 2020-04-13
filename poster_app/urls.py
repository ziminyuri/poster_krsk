from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth_user', views.auth_user, name='auth_user'),

    path('profile', views.profile, name='profile'),
    path('events', views.events, name='events'),
    path('booking', views.booking, name='booking'),

    path('concert', views.concert, name='concert'),
    path('conference', views.conference, name='conference'),
    path('exhibition', views.exhibition, name='exhibition'),
    path('theater', views.theater, name='theater'),


]
