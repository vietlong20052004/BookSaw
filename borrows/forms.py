from django import forms
from .models import BorrowRequest

class BorrowRequestApprovalForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        help_text="Optional: set the due date (default is 14 days from now)",
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = BorrowRequest
        fields = ['user', 'copy', 'status', 'due_date']
