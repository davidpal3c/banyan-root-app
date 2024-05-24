from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
    name            = models.CharField('Venue Name', max_length=120)
    address         = models.CharField(max_length=300)
    zip_code        = models.CharField('Zip Code', max_length=12)
    phone           = models.CharField('Contact Phone', max_length=25, blank=True)
    web             = models.URLField('Website Address', blank=True)
    email_address   = models.EmailField('Email', blank=True)
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Venue Owner')     # associates with user_id
    venue_image     = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name
    


class ClubUser (models.Model):
    first_name          = models.CharField(max_length=30)
    last_name           = models.CharField(max_length=30)
    email               = models.EmailField('User Email')
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name            = models.CharField('Event Name', max_length=150)
    event_date      = models.DateTimeField('Event date')
    venue           = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)   #connect Venue entity   
    manager         = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='managed_event')    # events linked to user won't be deleted if user is deleted 
    description     = models.TextField(blank=True)
    attendees       = models.ManyToManyField(User, blank=True, related_name='attended_events')  
    approved        = models.BooleanField('Approved', default=False, blank=True, null=True)
    event_image     = models.ImageField(upload_to="images/event_imgs/", null=True, blank=True)


    def __str__(self):
        return self.name
    

    # calculated field for days left until event
    @property
    def days_until(self):
        today = date.today()
        days_until = self.event_date.date() - today         # date of event minus today's date
        days_until_stripped = str(days_until).split(",", 1)[0]

        return days_until_stripped   


    @property
    def is_past(self):
        today = date.today()
        if self.event_date.date() < today:
            event_status = "Past"
            return event_status
        
        else:
            event_status = "Future"
            return event_status
        




        

