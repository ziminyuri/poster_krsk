from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserProfile(models.Model):
    ID_user_profile = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=17)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return self.surname + " " + self.name


class TypeEvent(models.Model):
    ID_type_event = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    plural_name = models.CharField(max_length=50)

    class Meta:
        db_table = "type_event"

    def __str__(self):
        return self.name


class TypeExhibition(models.Model):
    id_type_exhibition = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "type_exhibition"

    def __str__(self):
        return self.name


class EventStatus(models.Model):
    id_event_status = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "event_status"

    def __str__(self):
        return self.name


class Event(models.Model):
    ID_event = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=2000)
    phone = models.CharField(max_length=15, null=True, blank=True)
    data_begin = models.DateField(null=True, blank=True)
    data_end = models.DateField(null=True, blank=True)
    time_begin = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    isfree = models.BooleanField(default=True)
    ticket_price = models.CharField(max_length=15, null=True, blank=True)
    number_of_tickets = models.CharField(max_length=7, null=True, blank=True)
    ID_type_event = models.ForeignKey(TypeEvent, models.DO_NOTHING)
    ID_user_profile = models.ForeignKey(UserProfile, models.DO_NOTHING)

    user_name: str = str(ID_user_profile.name)
    img = models.ImageField(
        upload_to=(user_name + "events"), default=settings.MEDIA_URL + "defualt.jpg"
    )
    id_type_exhibition = models.ForeignKey(
        TypeExhibition, models.DO_NOTHING, blank=True, null=True
    )
    id_event_status = models.ForeignKey(
        EventStatus, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        db_table = "event"

    def __str__(self):
        return self.name
