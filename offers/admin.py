from django.contrib import admin
from .models import Destination, Offer

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('nom_destination', 'pays', 'saison')
    search_fields = ('nom_destination', 'pays')
    list_filter = ('pays', 'saison')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix_par_personne', 'actif')
    list_filter = ('actif',)
    search_fields = ('titre', 'description', 'nom_destinations__nom_destination')
    filter_horizontal = ('nom_destinations',)
    ordering = ('titre',)