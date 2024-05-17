from django.urls import path
from . import views


app_name = "events"

urlpatterns = [
   
    # path('', views.home, name='home')
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events/', views.events_all, name='event-list'),
     # path converters: int, str, path (whole urls/), slugs (hyphen-and_unerscores), UUID
    path('add_venue/', views.add_venue, name='add-venue'),
]
