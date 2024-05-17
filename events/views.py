from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime

from django.http import HttpResponseRedirect    # redirect_lazy change (redirect back to the page itself)
from .models import Event, Venue
from .forms import VenueForm




def search_venues(request):    
    if request.method == "POST":  
        searched = request.POST['searched']
        
        # query database for search
        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues})
    
    else: 
        return render(request, 'events/search_venues.html', {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', {'venue': venue})


def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 'events/venues.html', {'venue_list': venue_list})


def add_venue(request):
    submitted = False           # default variable for submit
    
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')        # sends submitted variable into get request

    else:   
        form = VenueForm
        if 'submitted' in request.GET:              # submitted variable found in GET request
            submitted = True


    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


# pull data from database
def events_all(request):
    event_list = Event.objects.all()

    return render(request, 'events/event_list.html', 
                  {'event_list': event_list})


def home(request, year, month):
    name = "Moe"
    month = month.capitalize()

    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # get current year
    now = datetime.now()
    current_year = now.year 

    # get current time
    time = now.strftime('%I:%M: %p')

    return render(request, 'core/home.html',
                   {"name": name,
                    "year": year,
                    "month": month,
                    "month_number": month_number,
                    "cal": cal,
                    "current_year": current_year,
                    "time": time,
                    })


