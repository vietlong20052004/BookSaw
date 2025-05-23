from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from books.models import BookCopy
from .models import Loan, BorrowRequest
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def request_borrow(request, copy_id):
    """
    When a user clicks “Request Copy”, create a Loan for that BookCopy
    (in a real system you’d create a pending BorrowRequest and wait
    for staff approval; here we immediately loan it for 14 days).
    """
    copy = get_object_or_404(BookCopy, id=copy_id)

    if not copy.is_available:
        messages.error(request, "Sorry, that copy is not available right now.")
        return redirect('books:detail', pk=copy.book.pk)

        # Create the borrow request
    br = BorrowRequest.objects.create(
            user=request.user,
            copy=copy,
            status='PENDING'
        )

    # Notify the user that their request is being handled
    Notification.objects.create(
            user=request.user,
            message=(
                f"Your borrow request for “{copy.book.title}” is pending approval."
            ),
            url= reverse('books:detail', args=[copy.book.pk])
        )

    return redirect('borrows:my_loans')

@login_required
def my_loans(request):
    """
    Show the current user’s active and past loans.
    """
    loans = Loan.objects.filter(user=request.user).order_by('-borrow_date')
    requests = BorrowRequest.objects.filter(
        user=request.user,
        status=BorrowRequest.STATUS_PENDING
    ).order_by('-created_at')
    return render(request, 'borrows/my_loans.html', {
        'loans': loans,
        'requests':requests,
    })

@login_required
def return_loan(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id, user=request.user)
    if loan.returned_date is None:
        loan.mark_returned()
        # Notify the user
        Notification.objects.create(
            user    = request.user,
            message = f"✅ You’ve returned “{loan.copy.book.title}”. Thanks!",
            url     = reverse('borrows:my_loans')
        )
    return redirect('borrows:my_loans')


