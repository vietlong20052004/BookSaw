from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_redirect(request, pk):
    """
    Marks the notification as read and redirects to its URL.
    """
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    # mark as read
    if not notif.is_read:
        notif.is_read = True
        notif.save(update_fields=['is_read'])
    # redirect to the stored URL (could be internal or external)
    return redirect(notif.url)
