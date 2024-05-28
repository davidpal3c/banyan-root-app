from django.urls import path
from . import views


app_name = "events"

urlpatterns = [
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('', views.redirect_to_home, name='redirect-to-home'),
    path('events/', views.all_events, name='list-events'),
    path('venues/', views.list_venues, name='list-venues'),
    path('add_event/', views.add_event, name='add-event'),
    path('add_venue/', views.add_venue, name='add-venue'),    # path converters: int, str, path (whole urls/), slugs (hyphen-and_unerscores), UUID
    path('show_venue/<venue_id>/', views.show_venue, name='show-venue'),
    path('venue_events/<venue_id>', views.venue_events, name='venue-events'),
    path('search/', views.search, name='search'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),
    path('my_events', views.my_events, name='my-events'),
    path('join_event/<int:event_id>/', views.join_event, name='join-event'),
    path('leave_event/<int:event_id>/', views.leave_event, name='leave-event'),
    path('search_events', views.search_events, name='search-events'),
    path('admin_approval', views.admin_approval, name='admin-approval'),
    path('show_event/<event_id>/', views.show_event, name='show-event'),    
    path('privacy_policy/', views.privacy_policy, name='privacy-policy'),    
    path('terms_of_service/', views.terms_of_service, name='terms-of-service'),    
]
