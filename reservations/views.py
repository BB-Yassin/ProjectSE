from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from .models import Reservation 
from .forms import ReservationForm 
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from offers.models import Offer


def home(request):
    return HttpResponse("Bienvenue dans l’application de réservations.")

class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/creer_reservations.html'

    def dispatch(self, request, *args, **kwargs):
        # Récupérer l'offre depuis l'URL
        self.offre = get_object_or_404(Offer, id=kwargs['offre_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Associer automatiquement l'offre
        form.instance.offre = self.offre
        response = super().form_valid(form)

        # Envoyer mail
        send_mail(
            'Confirmation de réservation',
            f'Votre réservation {self.object.id_reservation} pour l\'offre "{self.offre.titre}" a été enregistrée.',
            'from@example.com',
            [self.object.client.email],
            fail_silently=True
        )

        messages.success(self.request, "Un email de confirmation a été envoyé.")

        return response

    def get_success_url(self):
        return reverse_lazy('liste_reservations')

class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/modifier_reservation.html'
    success_url = reverse_lazy('liste_reservations')

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservations/supprimer_reservation.html'
    success_url = reverse_lazy('liste_reservations')  # Assurez-vous que cette URL existe

from django.views.generic import ListView
from .models import Reservation
from django.utils.dateparse import parse_date

class ReservationListView(ListView):
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'reservations/liste_reservations.html'

    def get_queryset(self):
        qs = super().get_queryset().select_related('client', 'offre')

        date_str = self.request.GET.get('date')
        mode = self.request.GET.get('mode_paiement')

        if date_str:
            d = parse_date(date_str)
            if d:
                qs = qs.filter(date_reservation__date=d)

        if mode:
            qs = qs.filter(mode_paiement=mode)

        return qs



class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'








