from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Inbox
from .forms import InboxForm, MessageForm


@login_required
def home(request):
    inboxes = Inbox.objects.filter(Q(owner=request.user) | Q(guess=request.user))
    inbox = inboxes.order_by('-updated_at').first()
    if not inbox:
        return render(request, 'inbox/inboxes.html', {})
    else:
        return redirect('view-inbox', pk=inbox.pk)


@login_required
def view_inbox(request, pk):
    inboxes = Inbox.objects.filter(Q(owner=request.user) |
                                   Q(guess=request.user)).order_by('-updated_at')
    inbox = Inbox.objects.get(pk=pk)
    if (request.user == inbox.owner) or (request.user == inbox.guess):
        messages = inbox.messages.all()
        # Mark with read=True all the messages from the other user
        for message in messages.filter(Q(read=False) & ~Q(user=request.user)):
            message.read = True
            message.save()
        form = MessageForm()
        return render(request, 'inbox/inbox-view.html', {'inbox': inbox, 'inboxes': inboxes,
                                                         'form': form, 'messages': messages})
    else:
        return HttpResponse(status=403)


@login_required
def new_inbox(request):
    if request.method == 'POST':
        form = InboxForm(request.user, request.POST)
        if form.is_valid():
            inbox = form.save(commit=False)
            inbox.owner = request.user
            inbox.save()
            return redirect('home')
    else:
        form = InboxForm(request.user)
    return render(request, 'inbox/new-inbox.html', {'form': form})


@login_required
def new_message(request, pk):
    inbox = Inbox.objects.get(pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.inbox = inbox
            message.save()

        return redirect('view-inbox', pk=inbox.pk)
    else:
        return HttpResponse(status=403)
