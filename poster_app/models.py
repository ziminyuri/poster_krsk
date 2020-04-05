from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    ID_user_profile = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=17)

    class Meta:
        db_table = 'user_profile'


class TypeEvent(models.Model):
    ID_type_event = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'type_event'


class Event(models.Model):
    ID_event = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    img_path = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    data_time = models.DateTimeField()
    ticket_price = models.CharField(max_length=15)
    number_of_tickets = models.CharField(max_length=7)
    ID_type_event = models.ForeignKey(TypeEvent, models.DO_NOTHING)
    ID_user_profile = models.ForeignKey(UserProfile, models.DO_NOTHING)

    class Meta:
        db_table = 'event'


