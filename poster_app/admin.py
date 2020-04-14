from django.contrib import admin
from .models import UserProfile, TypeEvent, Event, TypeExhibition, EventStatus

admin.site.register(TypeEvent)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(TypeExhibition)
admin.site.register(EventStatus)
