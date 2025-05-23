from .models import User
from django.utils import timezone
from borrows.models import Loan


def notifications(request):
    """
    Adds `notifications` (all) and `unread_notifications_count` to the template context.
    """
    if request.user.is_authenticated:
        qs = request.user.notifications.all()
        return {
            'notifications': qs,
            'unread_notifications_count': qs.filter(is_read=False).count(),
        }
    return {}

def overdue_warnings(request):
    if request.user.is_authenticated:
        overdue = Loan.objects.filter(
            user=request.user,
            due_date__lt=timezone.now(),
            returned_date__isnull=True
        )
        return {
            'overdue_loans_count': overdue.count(),
            'overdue_loans': overdue,
        }
    return {}