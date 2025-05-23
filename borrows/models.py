# borrows/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from books.models import BookCopy
from datetime import timedelta


class Loan(models.Model):
    """
    Represents an approved book loan.
    A Loan is created when a staff member approves a borrow request.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loans',
        help_text="The user who borrowed the book."
    )
    copy = models.ForeignKey(
        BookCopy,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    borrow_date = models.DateTimeField(
        auto_now_add=True,
        help_text="When the book was borrowed."
    )
    due_date = models.DateTimeField(
        help_text="When the book is due back."
    )
    returned_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the book was actually returned. Null if not yet returned."
    )

    # Optional audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-borrow_date']
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f"Loan #{self.pk}: {self.copy} to {self.user}"
    @property
    def is_returned(self) -> bool:
        """True if the book has been returned."""
        return self.returned_date is not None

    @property
    def is_overdue(self) -> bool:
        """True if today is past due_date and the book is not returned yet."""
        if self.returned_date:
            return False
        return timezone.now() > self.due_date

    @property
    def overdue_days(self) -> int:
        """
        Number of days overdue.
        Returns 0 if not overdue or already returned on time.
        """
        if not self.is_overdue:
            return 0
        delta = timezone.now() - self.due_date
        return delta.days

    def mark_returned(self):
        """
        Record the return and free up the copy.
        """
        if not self.returned_date:
            self.returned_date = timezone.now()
            self.save(update_fields=['returned_date'])
            # mark the copy available again
            self.copy.is_available = True
            self.copy.save(update_fields=['is_available'])
        return self

class BorrowRequest(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='borrow_requests')
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE,
                             related_name='borrow_requests')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def approve(self, due_date=None):
        """
        Approve this request:
        1) Create a Loan (2-week default)
        2) Mark the BookCopy unavailable
        3) Update status to APPROVED
        Returns the Loan instance.
        """
        now = timezone.now()
        if due_date is None:
            due_date = now + timedelta(days=14)

        # create the loan record
        loan = Loan.objects.create(
            user=self.user,
            copy=self.copy,
            borrow_date=now,
            due_date=due_date
        )

        # mark the copy as checked out
        self.copy.is_available = False
        self.copy.save(update_fields=['is_available'])

        # 3) mark request approved
        self.status = self.STATUS_APPROVED
        self.save(update_fields=['status'])

        return loan

    def __str__(self):
        return f"{self.user} → {self.copy} [{self.status}]"
