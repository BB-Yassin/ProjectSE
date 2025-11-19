# booking/models.py
from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'Refunded'

class PaymentMethod(models.TextChoices):
    CARD = 'CARD', 'Card'
    PAYPAL = 'PAYPAL', 'PayPal'
    BANK_TRANSFER = 'BANK', 'Bank Transfer'
    CASH = 'CASH', 'Cash'

class Payment(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode_paiement = models.CharField(max_length=20, choices=PaymentMethod.choices)
    date_transaction = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    devise = models.CharField(max_length=5, default='USD')
    transaction_reference = models.CharField(max_length=128, blank=True, null=True)

    def refund(self, reason: str = ''):
        # placeholder: your real gateway/refund logic goes here
        if self.statut == PaymentStatus.COMPLETED:
            self.statut = PaymentStatus.REFUNDED
            self.save()
            # log refund reason or trigger webhook
            return True
        return False

    def verifier_paiement(self):
        # placeholder: integrate with provider to verify status
        # set statut accordingly and save
        return self.statut

    def __str__(self):
        return f"{self.montant} {self.devise} ({self.statut})"

class ReservationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    COMPLETED = 'COMPLETED', 'Completed'

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    offer = models.ForeignKey('offers.Offer', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    customer_info = models.ForeignKey('customers.CustomerInfo', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    date_reservation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    nbr_personnes = models.PositiveIntegerField(default=1)
    date_depart = models.DateField(null=True, blank=True)
    date_retour = models.DateField(null=True, blank=True)
    reference_paiement = models.CharField(max_length=128, blank=True, null=True)
    payment = models.OneToOneField('booking.Payment', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservation')

    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def annuler(self, reason: str = ''):
        self.status = ReservationStatus.CANCELLED
        self.cancelled_at = timezone.now()
        self.save()
        # optionally issue refund via payment
        if self.payment:
            self.payment.refund(reason)
        return self

    def modifier(self, **kwargs):
        # update allowed fields (safe set)
        allowed = {'date_depart', 'date_retour', 'nbr_personnes', 'prix_total', 'customer_info'}
        changed = False
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)
                changed = True
        if changed:
            self.save()
        return self

    def confirmer(self, payment: Payment = None):
        self.status = ReservationStatus.CONFIRMED
        self.confirmed_at = timezone.now()
        if payment:
            self.payment = payment
            self.reference_paiement = payment.transaction_reference or self.reference_paiement
        self.save()
        return self

    def __str__(self):
        return f"Reservation #{self.id} by {self.user.get_full_name()} - {self.status}"
