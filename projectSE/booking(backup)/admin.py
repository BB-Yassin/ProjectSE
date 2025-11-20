# booking/admin.py
from django.contrib import admin
from .models import Reservation, Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'montant', 'devise', 'methode_paiement', 'statut', 'date_transaction')
    search_fields = ('transaction_reference',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'offer', 'status', 'prix_total', 'date_reservation')
    list_filter = ('status', 'date_reservation')
    search_fields = ('reference_paiement', 'user__email')
