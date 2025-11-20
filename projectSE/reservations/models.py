# reservations/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ]

    id_reservation = models.AutoField(primary_key=True)
    date_reservation = models.DateTimeField(auto_now_add=True)
    statut_reservation = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    nb_personnes = models.PositiveIntegerField()
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    offre = models.ForeignKey(
        'offers.Offer',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if self.offre and self.nb_personnes:
            self.prix_total = self.offre.prix_base * self.nb_personnes
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name} - {self.date_reservation}"

class Paiement(models.Model):
    MODE_CHOICES = [
        ('carte_bancaire', 'Carte bancaire'),
        ('virement_bancaire', 'Virement bancaire'),
        ('paypal', 'PayPal'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('echoue', 'Échoué'),
    ]

    id_paiement = models.AutoField(primary_key=True)
    delai_paiement = models.DateField(null=True, blank=True)
    mode_paiement = models.CharField(max_length=20, choices=MODE_CHOICES)
    statut_paiement = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_transaction = models.DateTimeField(null=True, blank=True)

    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='paiement'
    )

    def save(self, *args, **kwargs):
        if self.reservation and not self.delai_paiement:
            self.delai_paiement = self.reservation.date_reservation + timedelta(days=7)
        if self.statut_paiement == 'paye' and self.date_transaction is None:
            self.date_transaction = timezone.now()
        super().save(*args, **kwargs)
