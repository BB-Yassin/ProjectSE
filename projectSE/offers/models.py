# offers/models.py
from django.db import models
from django.utils import timezone

class AccommodationCategory(models.TextChoices):
    HOTEL = 'HOTEL', 'Hotel'
    APARTMENT = 'APARTMENT', 'Apartment'
    VILLA = 'VILLA', 'Villa'

class Accommodation(models.Model):
    type = models.CharField(max_length=50)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=AccommodationCategory.choices, default=AccommodationCategory.HOTEL)
    capacite = models.PositiveIntegerField(default=2)
    equipement = models.TextField(blank=True)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.adresse}, {self.ville}"

class Flight(models.Model):
    compagnie = models.CharField(max_length=100)
    numero_vol = models.CharField(max_length=50)
    aeroport_arrive = models.CharField(max_length=100)
    aeroport_depart = models.CharField(max_length=100, blank=True, null=True)
    date_depart = models.DateTimeField()
    date_arrive = models.DateTimeField()
    duree = models.DurationField(null=True, blank=True)
    classe_disponibles = models.CharField(max_length=100, blank=True)
    bagage_inclus = models.BooleanField(default=False)
    terminal_depart = models.CharField(max_length=50, blank=True, null=True)
    terminal_arrive = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.compagnie} {self.numero_vol} ({self.date_depart:%Y-%m-%d %H:%M})"

class OfferType(models.TextChoices):
    PACKAGE = 'PACKAGE', 'Package'
    FLIGHT_ONLY = 'FLIGHT', 'Flight'
    ACCOMMODATION_ONLY = 'ACCOM', 'Accommodation'

class Offer(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type_offre = models.CharField(max_length=20, choices=OfferType.choices, default=OfferType.PACKAGE)
    prix_base = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilite = models.PositiveIntegerField(default=1)
    politique_remboursement = models.TextField(blank=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True, related_name='offers')
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True, related_name='offers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
