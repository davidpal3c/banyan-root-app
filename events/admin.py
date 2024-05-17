from django.contrib import admin
from .models import ClubUser, Event, Venue


admin.site.register(ClubUser)
# admin.site.register(Event)
# admin.site.register(Venue)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address', 'email_address')
    # search_fields = ('__all__')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'attendees')
    list_display = ('name', 'event_date', 'venue')  # event page columns 
    list_filter = ('event_date', 'venue')           # main page list change
    ordering = ('-event_date',)                     # event date column value listed from year-> day