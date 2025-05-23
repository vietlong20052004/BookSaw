from django.contrib import admin
from django.utils import timezone
from .models import BorrowRequest, Loan
from notifications.models import Notification
from django.urls import reverse
from .models import BorrowRequest
from .forms import BorrowRequestApprovalForm

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    form = BorrowRequestApprovalForm

    list_display  = ('user', 'copy',  'status', 'created_at')
    list_filter   = ('status',)
    actions       = ['approve_requests', 'reject_requests']

    @admin.action(description="Approve selected requests")
    def approve_requests(self, request, queryset):
        for br in queryset.filter(status=BorrowRequest.STATUS_PENDING):
            loan = br.approve(approver=request.user)
            # notify the user
            Notification.objects.create(
                user=br.user,
                message=f"✅ Your borrow request for “{br.copy.book.title}” was approved. Due on {loan.due_date.date()}.",
                url=reverse('borrows:my_loans')
            )

    @admin.action(description="Reject selected requests")
    def reject_requests(self, request, queryset):
        for br in queryset.filter(status=BorrowRequest.STATUS_PENDING):
            br.status = BorrowRequest.STATUS_REJECTED
            br.save(update_fields=['status'])
            Notification.objects.create(
                user=br.user,
                message=f"❌ Your borrow request for “{br.copy.book.title}” was rejected.",
                url=reverse('books:detail', args=[br.copy.book.pk])
            )

    def save_model(self, request, obj, form, change):
        """
               If admin manually changes status in the form, run
               approve() or send reject notification accordingly.
               """
        # Fetch original status before saving
        original_status = None
        if change:
            try:
                original = BorrowRequest.objects.get(pk=obj.pk)
                original_status = original.status
            except BorrowRequest.DoesNotExist:
                original_status = None

        # Save the updated obj first
        super().save_model(request, obj, form, change)

        # If status changed from PENDING → APPROVED, call approve()
        if change and original_status == BorrowRequest.STATUS_PENDING:
            if obj.status == BorrowRequest.STATUS_APPROVED:
                loan = obj.approve()
                Notification.objects.create(
                    user=obj.user,
                    message=(
                        f"✅ Your borrow request for “{obj.copy.book.title}” "
                        f"has been approved! Due on {loan.due_date.date()}."
                    ),
                    url=reverse('borrows:my_loans')
                )
            elif obj.status == BorrowRequest.STATUS_REJECTED:
                Notification.objects.create(
                    user=obj.user,
                    message=f"❌ Your borrow request for “{obj.copy.book.title}” was rejected.",
                    url=reverse('books:detail', args=[obj.copy.book.pk])
                )
