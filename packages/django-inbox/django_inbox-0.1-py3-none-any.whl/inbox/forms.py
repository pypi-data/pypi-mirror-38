from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Inbox, Message


class InboxForm(ModelForm):
    class Meta:
        model = Inbox
        fields = ['guess']

    def __init__(self, user, *args, **kwargs):
        super(InboxForm, self).__init__(*args, **kwargs)
        self.fields['guess'].queryset = User.objects.exclude(pk=user.pk)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['content']
