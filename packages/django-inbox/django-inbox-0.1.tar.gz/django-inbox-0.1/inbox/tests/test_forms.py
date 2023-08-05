from django.contrib.auth.models import User
from django.test import TestCase

from inbox.models import Inbox
from inbox.forms import InboxForm, MessageForm


class SetupClass(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='test')
        self.guess = User.objects.create_user(username='guess', password='test')
        self.inbox = Inbox.objects.create(owner=self.owner, guess=self.guess)
        self.client.login(username='owner', password='test')


class InboxFormTest(SetupClass):
    def test_inbox_form_valid(self):
        data = {'guess': self.guess.pk}
        form = InboxForm(user=self.owner, data=data)
        self.assertTrue(form.is_valid())


class MessageFormTest(SetupClass):
    def test_message_form_valid(self):
        data = {'content': 'Hello'}
        form = MessageForm(data=data)
        self.assertTrue(form.is_valid())
