from django import forms
from django.forms import ModelForm
from .models import Venue, ClubUser, Event

# User Event Form
class EventForm(ModelForm):
    class Meta:
        model = Event   
        fields = ('name', 'event_date', 'venue', 'attendees', 'description','event_image')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
            'event_image': '',
        }
        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            
        }

# Admin SuperUser Event Form
class AdminEventForm(ModelForm):
    class Meta:
        model = Event   
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description', 'event_image')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
            'event_image': '',
        }
        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class VenueForm(ModelForm):
    class Meta:
        model = Venue   
        # fields = '__all__'
        fields = ('name', 'address', 'city_state', 'country', 'zip_code', 'phone', 'web', 'email_address', 'venue_image', 'owner')
        labels = {
            'name': '',
            'address': '',
            'city_state':'',
            'country':'',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue_image':'',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Web Address'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'owner': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue Owner'}),
        }
