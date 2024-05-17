from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name            = models.CharField('Venue Name', max_length=120)
    address         = models.CharField(max_length=300)
    zip_code        = models.CharField('Zip Code', max_length=12)
    phone           = models.CharField('Contact Phone', max_length=25, blank=True)
    web             = models.URLField('Website Address', blank=True)
    email_address   = models.EmailField('Email', blank=True)


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
    manager         = models.ForeignKey(User, blank=True, null= True, on_delete=models.SET_NULL)    # events linked to user won't be deleted if user is deleted 
    description     = models.TextField(blank=True)
    attendees       = models.ManyToManyField(ClubUser, blank=True)
 
    def __str__(self):
        return self.name
    