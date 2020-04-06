from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth_user', views.auth_user, name='auth_user')
]
