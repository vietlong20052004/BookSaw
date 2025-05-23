# notifications/admin.py

from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('user', 'message', 'url', 'is_read', 'created_at')
    list_filter   = ('is_read', 'created_at', 'user')
    search_fields = ('message', 'user__username')
    ordering      = ('-created_at',)
    actions       = ['mark_as_read', 'mark_as_unread']

    @admin.action(description="Mark selected notifications as read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked read.")

    @admin.action(description="Mark selected notifications as unread")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notification(s) marked unread.")
