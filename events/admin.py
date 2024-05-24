from django.contrib import admin
from .models import ClubUser, Event, Venue
from django.contrib.auth.models import Group, User

admin.site.register(ClubUser)
# admin.site.register(Event)
# admin.site.register(Venue)

# Remove Group from admin
# admin.site.unregister(Group)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email_address', 'owner')
    ordering = ('name',)
    search_fields = ('name', 'address', 'email_address')
    



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'event_image', 'manager', 'attendees', 'approved')
    list_display = ('name', 'event_date', 'venue')  # event page columns 
    list_filter = ('event_date', 'venue')           # main page list change
    ordering = ('-event_date',)                     # event date column value listed from year-> day



    # def event_image_thumbnail(self, obj):
    #     if obj.event_image:
    #         return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.event_image.url))
    #     return ''
    
    # event_image_thumbnail.short_description = 'Event Image'