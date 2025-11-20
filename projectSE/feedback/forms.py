# feedback/forms.py
from django import forms
from .models import Feedback
from offers.models import Offer

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['offer', 'note', 'description', 'attachement']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us about your experience...'}),
            'note': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def clean_note(self):
        note = self.cleaned_data.get('note')
        if note is None:
            return None
        if not (1 <= note <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return note
