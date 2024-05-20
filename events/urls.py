from django.urls import path
from . import views


app_name = "events"

urlpatterns = [
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events/', views.all_events, name='list-events'),
    path('venues/', views.list_venues, name='list-venues'),
    path('add_event/', views.add_event, name='add-event'),
    path('add_venue/', views.add_venue, name='add-venue'),    # path converters: int, str, path (whole urls/), slugs (hyphen-and_unerscores), UUID
    path('show_venue/<venue_id>/', views.show_venue, name='show-venue'),
    path('search_venues/', views.search_venues, name='search-venues'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text', views.venue_text , name='venue-text'),
    path('venue_csv', views.venue_csv , name='venue-csv'),
    path('venue_pdf', views.venue_pdf , name='venue-pdf'),
    path('my_events', views.my_events , name='my-events'),
]
