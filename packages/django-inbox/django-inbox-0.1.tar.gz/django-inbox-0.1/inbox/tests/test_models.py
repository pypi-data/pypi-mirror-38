from django.contrib.auth.models import User
from django.test import TestCase

from inbox.models import Inbox, Message


class SetupClass(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='test')
        self.guess = User.objects.create_user(username='guess', password='test')
        self.inbox = Inbox.objects.create(owner=self.owner, guess=self.guess)


class InboxTest(SetupClass):
    def test_inbox_creation(self):
        self.assertTrue(isinstance(self.inbox, Inbox))
        self.assertEqual(str(self.inbox), 'owner - guess')
        self.assertEqual(self.inbox.owner, self.owner)
        self.assertEqual(self.inbox.guess, self.guess)


class MessageTest(SetupClass):
    def test_message_creation(self):
        message = Message.objects.create(inbox=self.inbox, user=self.owner, content='Hello world')
        self.assertTrue(isinstance(message, Message))
        self.assertEqual(message.user, self.owner)
        self.assertEqual(message.content, 'Hello world')
        self.assertFalse(message.read)
