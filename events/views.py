from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count

import calendar
from calendar import HTMLCalendar
from datetime import datetime, timedelta
from django.utils import timezone

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse    # redirect_lazy change (redirect back to the page itself)
from .models import Event, Venue
from django.contrib.auth.models import User

from .forms import VenueForm, EventForm, AdminEventForm
from django.contrib import messages
import csv

# search / django-haystack
from django.db.models import Q


# pdf functionality modules
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io 

# pagination
from django.core.paginator import Paginator


def privacy_policy(request):
    return render(request, 'events/privacy_policy.html')


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


@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.attendees.remove(request.user)
    event_name = event.name

    messages.success(request, (f"You have Unregistered from the '{event_name}' event..."))
    return redirect('events:show-event', event_id=event.id)




@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.attendees.add(request.user)
    
    messages.success(request, ("You have Registered Successfully for this event..."))

    return redirect('events:show-event', event_id=event.id)



def my_events(request):
    if request.user.is_authenticated:
        user = request.user.id
        events = Event.objects.filter(attendees=user)
        has_events = events.exists()
        # managed_events = Event.objects.filter()

        return render(request, 'events/my_events.html', 
                      {"events":events,
                       "has_events": has_events})

    else:
        messages.success(request, ("You aren't Authorized to View this Page."))
        return redirect('events:list-events')
 


 
def search_events(request):
    if request.method == "POST":  
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)      # query database for search

        return render(request, 'events/search_events.html', 
                      {'searched': searched,
                       'events': events})
    
    else: 
        return render(request, 'events/search_events.html', {})


def search(request):
    query = request.GET.get('q', '')
    if query:
        # Search in Event model
        events = Event.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        # Search in Venue model
        venues = Venue.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(zip_code__icontains=query)
        )
        return render(request, 'events/search_results.html', {'query': query, 'events': events, 'venues': venues})





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
    messages.success(request, ("Venue Deleted!"))
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
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    
    if form.is_valid():
        form.save()
        return redirect('events:list-venues')

    return render(request, 'events/update_venue.html', 
                  {'venue': venue,
                   'form': form})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = AdminEventForm(request.POST or None, request.FILES or None, instance=event)
    else:
        form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('events:list-events')

    return render(request, 'events/update_event.html', 
                  {'event': event,
                   'form': form})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)

    venue_owner = Venue.owner     # venue owner query | non-primary model attribute alternative

    print(venue_owner)
    # Get events for particular venue
    events = venue.event_set.all()  

    return render(request, 'events/show_venue.html', 
                  {'venue': venue,
                   'venue_owner': venue_owner,
                   'events': events})


# Show Event
def show_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    event_list = Event.objects.all().order_by('event_date')

    event_with_attendee_count = Event.objects.annotate(num_attendees=Count('attendees'))
    attendee_count = event_with_attendee_count.count()

    return render(request, 'events/show_event.html', 
                  {"event": event,
                   "event_list": event_list,
                   "attendee_count": attendee_count})


# Events per Venue
def venue_events(request, venue_id):
    # Lookup venue
    venue = Venue.objects.get(id=venue_id)
    # Get venue events
    events = venue.event_set.all()           # grab events associated with venue (id)
    # events_list = Event.objects.filter(pk=venue_id)

    # print(f"THIS IS THE EVENT LIST LOG: {events_list}")


    if events:
        return render(request, 'events/venue_events.html', 
                      {"events": events})
    
    else:
        messages.success(request, ("That Venue Has No Events At This Time..."))
        return redirect('events:admin-approval')



def admin_approval(request):

    # Get venues
    venue_list = Venue.objects.all().order_by('name')

    # Get counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')     # get list with event_id of checked boxes (named 'boxes)
            # print(id_list)            # debugging log

            # Uncheck all events
            event_list.update(approved=False)
            
            # # Update database
            for i in id_list:
                Event.objects.filter(pk=int(i)).update(approved=True)       # updates approve to true, by filtering pk of event.id in box 

            # Shows success Message and Redirects to url
            messages.success(request, ('Event List Approval Updated.'))
            return redirect('events:list-events')
        
        else:
            return render(request, 'events/admin_approval.html', 
                          {"event_list": event_list,
                           "event_count": event_count,
                           "venue_count": venue_count,
                           "user_count": user_count,
                           "venue_list": venue_list})
        
    else: 
        messages.success(request, ('Administrator Permission is required to access this page'))
        return redirect('events:list-events')
    

    return render(request, 'events/admin_approval.html')


def add_venue(request):
    submitted = False           # default variable for submit
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user      # assigns user id as model attribute

            # print(request.FILES)        # debugging log
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
            form = AdminEventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')        # sends submitted variable into get request

        else: 
            form = EventForm(request.POST, request.FILES)
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
    ordered_venues = Venue.objects.all().order_by('name')       # order by random ='?'
 
    p = Paginator(ordered_venues, 4)
    page = request.GET.get('page')
    venues = p.get_page(page)
    page_range = range(1, venues.paginator.num_pages + 1) 
    
 

    return render(request, 'events/venues.html', 
                  {'venues': venues,
                   'page_range': page_range})
    # return render(request, 'events/venues.html', {'venue_list': venue_list, 'venues':venues})



def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    

    event_with_attendee_count = Event.objects.annotate(num_attendees=Count('attendees'))
    attendee_count = {event.id: event.num_attendees for event in event_with_attendee_count}

    return render(request, 'events/event_list.html', 
                  {'event_list': event_list,
                   'attendee_count': attendee_count})





def home(request, year=None, month=None):
    # Default to the current year and month if none are provided
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().strftime('%B')

    # Convert month name to month number
    try:
        month_number = list(calendar.month_name).index(month.capitalize())
    except ValueError:
        month_number = timezone.now().month


    
    # Create a datetime object for easier month navigation
    current_date = datetime(year, month_number, 1)

    # Calculate previous and next months
    prev_month = (current_date - timedelta(days=1)).strftime('%B')
    prev_year = (current_date - timedelta(days=1)).year
    next_month = (current_date + timedelta(days=32)).strftime('%B')
    next_year = (current_date + timedelta(days=32)).year


    cal = HTMLCalendar().formatmonth(year, month_number)

    current_year = timezone.now().year
    current_time = timezone.now().strftime('%I:%M: %p')

    # Query events model for the specified date
    event_list = Event.objects.filter(event_date__year=year, event_date__month=month_number)
    
    

    context = {
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": current_time,
        "event_list": event_list,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    }

    return render(request, 'events/home.html', context)



def redirect_to_home(request):
    current_month = timezone.now().strftime('%B')
    current_year = timezone.now().year
    return redirect('events:home', year=current_year, month=current_month)