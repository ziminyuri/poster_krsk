from django.contrib import admin
from .models import UserProfile, TypeEvent, Event, TypeExhibition, EventStatus, Setting, Booking, Ticket, StatusBooking,\
    TypeTicket


admin.site.register(TypeEvent)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(TypeExhibition)
admin.site.register(EventStatus)
admin.site.register(Setting)
admin.site.register(Booking)
admin.site.register(Ticket)
admin.site.register(StatusBooking)
admin.site.register(TypeTicket)

