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
        



class ReservationClientForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['offre', 'nb_personnes']  # client et prix_total ne sont pas exposés

class PaiementClientForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['mode_paiement']  # reservation et statut ne sont pas exposés