from django.contrib import admin

from .models import Inbox, Message


@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
