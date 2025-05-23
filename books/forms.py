from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ('rating','review')
        widgets = {
            'rating': forms.RadioSelect(),
            'review_text': forms.Textarea(attrs={'rows':4, 'placeholder': 'Write your thoughts…'}),
        }
