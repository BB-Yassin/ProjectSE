from django.contrib import admin
from .models import Reservation , Paiement


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id_reservation', 'client', 'offre', 'nb_personnes', 'prix_total', 'statut_reservation')
    list_filter = ('statut_reservation',)
    search_fields = ('client__nom', 'client__prenom')

class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id_paiement', 'reservation', 'mode_paiement', 'statut_paiement', 'delai_paiement', 'date_transaction')

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Paiement, PaiementAdmin)




