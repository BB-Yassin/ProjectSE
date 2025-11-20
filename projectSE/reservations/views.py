from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Reservation , Paiement
from .forms import ReservationForm , PaiementForm , ReservationClientForm , PaiementClientForm
from django.shortcuts import get_object_or_404

def home(request):
    return HttpResponse("Bienvenue dans l’application de réservations.")

def creer_reservation(request):
    prix_total = None
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.prix_total = reservation.offre.prix * reservation.nb_personnes
            reservation.save()
            return redirect('liste_reservations')
    else:
        form = ReservationForm()
    return render(request, 'reservations/creer_reservations.html', {'form': form})

def liste_reservations(request): #lire les reservations
    reservations = Reservation.objects.all()
    return render(request, 'reservations/liste_reservations.html', {'reservations': reservations})

def modifier_reservation(request, id_reservation):
    reservation = get_object_or_404(Reservation, id_reservation=id_reservation)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('liste_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/modifier_reservation.html', {'form': form})

def supprimer_reservation(request, id_reservation):
    reservation = get_object_or_404(Reservation, id_reservation=id_reservation)
    if request.method == 'POST':
        reservation.delete()
        return redirect('liste_reservations')
    return render(request, 'reservations/supprimer_reservation.html', {'reservation': reservation})

def creer_paiement(request):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_paiements')
    else:
        form = PaiementForm()
    return render(request, 'reservations/creer_paiement.html', {'form': form})


def liste_paiements(request):
    paiements = Paiement.objects.all()
    return render(request, 'reservations/liste_paiements.html', {'paiements': paiements})


def modifier_paiement(request, id_paiement):
    paiement = get_object_or_404(Paiement, id_paiement=id_paiement)
    if request.method == 'POST':
        form = PaiementForm(request.POST, instance=paiement)
        if form.is_valid():
            form.save()
            return redirect('liste_paiements')
    else:
        form = PaiementForm(instance=paiement)
    return render(request, 'reservations/modifier_paiement.html', {'form': form})


def supprimer_paiement(request, id_paiement):
    paiement = get_object_or_404(Paiement, id_paiement=id_paiement)
    if request.method == 'POST':
        paiement.delete()
        return redirect('liste_paiements')
    return render(request, 'reservations/supprimer_paiement.html', {'paiement': paiement})


def creer_reservation_client(request):
    if request.method == 'POST':
        form = ReservationClientForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user
            reservation.save()
            return redirect('liste_reservations')
    else:
        form = ReservationClientForm()
    return render(request, 'reservations/creer_reservation_client.html', {'form': form})

def creer_paiement_client(request, reservation_id):
    reservation = get_object_or_404(Reservation, id_reservation=reservation_id, client=request.user)

    if request.method == 'POST':
        form = PaiementClientForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.reservation = reservation
            paiement.save()
            return redirect('liste_paiements')  # ou page confirmation
    else:
        form = PaiementClientForm()
    return render(request, 'reservations/creer_paiement_client.html', {'form': form, 'reservation': reservation})