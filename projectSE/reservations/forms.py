from django import forms
from .models import Reservation , Paiement

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['offre', 'client', 'nb_personnes']

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['reservation', 'mode_paiement']
        