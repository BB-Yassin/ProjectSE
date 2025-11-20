from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_reservations, name='liste_reservations'),
    path('creer/', views.creer_reservation, name='creer_reservation'),
    path('modifier/<int:id_reservation>/', views.modifier_reservation, name='modifier_reservation'),
    path('supprimer/<int:id_reservation>/', views.supprimer_reservation, name='supprimer_reservation'),
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    path('paiements/creer/', views.creer_paiement, name='creer_paiement'),
    path('paiements/modifier/<int:id_paiement>/', views.modifier_paiement, name='modifier_paiement'),
    path('paiements/supprimer/<int:id_paiement>/', views.supprimer_paiement, name='supprimer_paiement'),
    path('client/creer/', views.creer_reservation_client, name='creer_reservation_client'),
    path('client/<int:reservation_id>/paiement/creer/', views.creer_paiement_client, name='creer_paiement_client'),
]


