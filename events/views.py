from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count

import calendar
from calendar import HTMLCalendar
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse    # redirect_lazy change (redirect back to the page itself)
from .models import Event, Venue
# Imports User Model from Django
from django.contrib.auth.models import User

from .forms import VenueForm, EventForm, AdminEventForm
from django.contrib import messages
import csv

# pdf functionality modules
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io 

# pagination
from django.core.paginator import Paginator





# Generate Venue PDF file
def venue_pdf(request):
    buf = io.BytesIO()                            # Create Bytestream buffer
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)       # Create canvas
    textobj = c.beginText()                       # Create text object 
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 14)

    venues = Venue.objects.all()
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")
    

    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


# Generate Venue CSV file
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # create csv wrivter
    writer = csv.writer(response)

    # model designation
    venues = Venue.objects.all()

    # column headings to csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])


    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    
    return response 

# Generate Venue PDF file
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    # now = datetime.now()
    # current_year = now.year 

    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # model designation
    venues = Venue.objects.all()
    venue_catalog = ['Event-App \n', 'Current Venues: \n'] 
    
    for venue in venues:
        venue_catalog.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

    response.writelines(venue_catalog)
    return response 



def my_events(request):
    if request.user.is_authenticated:
        user = request.user.id
        events = Event.objects.filter(attendees=user)


        return render(request, 'events/my_events.html', 
                      {"events":events,})

    else:
        messages.success(request, ("You aren't Authorized to View this Page."))
        return redirect('events:list-events')


   


def search_venues(request):    
    if request.method == "POST":  
        searched = request.POST['searched']
        
        # query database for search
        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'events/search_venues.html', 
                      {'searched': searched,
                       'venues': venues})
    
    else: 
        return render(request, 'events/search_venues.html', {})


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('events:list-venues')



def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
  
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!"))
        return redirect('events:list-events')
    
    else:
        messages.success(request, ("You aren't Authorized to Delete This Event."))
        return redirect('events:list-events')


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)  
    form = VenueForm(request.POST or None, instance=venue)
    
    if form.is_valid():
        form.save()
        return redirect('events:list-venues')

    return render(request, 'events/update_venue.html', 
                  {'venue': venue,
                   'form': form})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = AdminEventForm(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('events:list-events')

    return render(request, 'events/update_event.html', 
                  {'event': event,
                   'form': form})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)      # venue owner query | non-primarey model attribute alternative

    return render(request, 'events/show_venue.html', 
                  {'venue': venue,
                   'venue_owner': venue_owner})



def add_venue(request):
    submitted = False           # default variable for submit
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id        # assigns user id as model attribute
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')        # sends submitted variable into get request

    else:   
        form = VenueForm
        if 'submitted' in request.GET:              # submitted variable found in GET request
            submitted = True


    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})



def add_event(request):
    submitted = False           # default variable for submit
    if request.method == "POST":
        if request.user.is_superuser:
            form = AdminEventForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')        # sends submitted variable into get request

        else: 
            form = EventForm(request.POST)
            if form.is_valid():
                # form.save()
                event = form.save(commit=False)
                event.manager = request.user       
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')        # sends submitted variable into get request

    else:   
        # Going to page, Not submitting
        if request.user.is_superuser:  
            form = AdminEventForm
        else:
            form = EventForm

        if 'submitted' in request.GET:              # submitted variable found in GET request
            submitted = True


    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('name')       # order by random ='?'
 
    # pagination setup
    p = Paginator(Venue.objects.all(), 3)
    page = request.GET.get('page')
    venues = p.get_page(page)
    page_range = range(1, venues.paginator.num_pages + 1) 

    return render(request, 'events/venues.html', {'venues': venues,'page_range': page_range})
    # return render(request, 'events/venues.html', {'venue_list': venue_list, 'venues':venues})



def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    event_with_attendee_count = Event.objects.annotate(num_attendees=Count('attendees'))

    attendee_count = {event.id: event.num_attendees for event in event_with_attendee_count}

    return render(request, 'events/event_list.html', 
                  {'event_list': event_list,
                   'attendee_count': attendee_count})



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

    return render(request, 'home',
                   {"name": name,
                    "year": year,
                    "month": month,
                    "month_number": month_number,
                    "cal": cal,
                    "current_year": current_year,
                    "time": time,
                    })


