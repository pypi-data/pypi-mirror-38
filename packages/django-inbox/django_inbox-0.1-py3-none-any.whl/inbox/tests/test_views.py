from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from inbox.models import Inbox


class HomeViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)


class SetupClass(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='test')
        self.guess = User.objects.create_user(username='guess', password='test')
        self.inbox = Inbox.objects.create(owner=self.owner, guess=self.guess)
        self.client.login(username='owner', password='test')


class InboxTest(SetupClass):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/inbox/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('view-inbox', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)


class NewInboxTest(SetupClass):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/new-inbox/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('new-inbox'))
        self.assertEqual(response.status_code, 200)

    def test_new_inbox_view(self):
        pass


class NewMessageTest(SetupClass):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.post('/new-message/1/')
        self.assertEqual(response.status_code, 302)

    def test_view_wrong_method(self):
        response = self.client.get('/new-message/1/')
        self.assertEqual(response.status_code, 403)
