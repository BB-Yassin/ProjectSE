from django import forms
from .models import Reclamation, ReclamationComment
from reservations.models import Reservation



class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['type_de_reclamation', 'description', 'priorite', 'reservation']  # reservation shown conditionally
        widgets = {
            'description': forms.Textarea(attrs={'required': True}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            from reservations.models import Reservation   # local
            self.fields['reservation'].queryset = Reservation.objects.filter(client=user)
        else:
            self.fields.pop('reservation', None)

            
class ReclamationCommentForm(forms.ModelForm):
    class Meta:
        model = ReclamationComment
        fields = ['description']
        widgets = {'description': forms.Textarea(attrs={'required': True})}
