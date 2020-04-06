from django.contrib import admin
from .models import UserProfile, TypeEvent, Event

admin.site.register(TypeEvent)
admin.site.register(UserProfile)
admin.site.register(Event)