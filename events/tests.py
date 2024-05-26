from django.test import TestCase
from django.urls import reverse
from.models import Event, Venue
from.views import (
    venue_pdf, venue_csv, venue_text, leave_event, join_event, my_events, search_events, search, search_venues,
    delete_venue, delete_event, update_venue, update_event, show_venue, show_event, venue_events, admin_approval,
    add_venue, add_event, list_venues, all_events, home, redirect_to_home
)
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile




class JoinEventViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.event = Event.objects.create(name='Test Event')

    def test_join_event_redirects_to_show_event(self):
        response = self.client.post(reverse('join_event', args=[self.event.id]))
        self.assertRedirects(response, reverse('show-event', args=[self.event.id]))
        self.event.refresh_from_db()
        self.assertIn(self.event.attendees.all(), self.user)


class LeaveEventViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.event = Event.objects.create(name='Test Event', attendees=[self.user])

    def test_leave_event_redirects_to_show_event(self):
        response = self.client.post(reverse('leave_event', args=[self.event.id]))
        self.assertRedirects(response, reverse('show-event', args=[self.event.id]))
        self.event.refresh_from_db()
        self.assertNotIn(self.event.attendees.all(), self.user)



class VenuePdfViewTest(TestCase):
    def test_venue_pdf_response(self):
        response = self.client.get(reverse('venue_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertEqual(response['content-disposition'], 'attachment; filename=venue.pdf')



class VenueCsvViewTest(TestCase):
    def test_venue_csv_response(self):
        response = self.client.get(reverse('venue_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/csv')
        self.assertEqual(response['content-disposition'], 'attachment; filename=venues.csv')

