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

    def __str__(self):
        return self.surname + " " + self.name


class TypeEvent(models.Model):
    ID_type_event = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'type_event'

    def __str__(self):
        return self.name


class Event(models.Model):
    ID_event = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255)
    img_path = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    data_time_begin = models.DateTimeField(null=True, blank=True)
    data_time_end = models.DateTimeField(null=True, blank=True)
    ticket_price = models.CharField(max_length=15, null=True, blank=True)
    number_of_tickets = models.CharField(max_length=7, null=True, blank=True)
    ID_type_event = models.ForeignKey(TypeEvent, models.DO_NOTHING)
    ID_user_profile = models.ForeignKey(UserProfile, models.DO_NOTHING)

    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.name

