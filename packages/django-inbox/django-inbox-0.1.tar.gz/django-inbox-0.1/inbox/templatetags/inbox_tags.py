from django import template
from django.db.models import Q

from inbox.models import Inbox

register = template.Library()


@register.simple_tag
def get_unread_messages(inbox, user):
    inbox = Inbox.objects.get(pk=inbox.pk)
    unread_messages = inbox.messages.filter(Q(read=False) & ~Q(user=user))
    return unread_messages.count()
