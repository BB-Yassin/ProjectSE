
from django.db import models
from django.conf import settings
from offers.models import Offer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils import send_reservation_email


class Reservation(models.Model):
    id_reservation = models.AutoField(primary_key=True)
    date_reservation = models.DateTimeField(auto_now_add=True)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    nb_personnes = models.PositiveIntegerField()
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offer, on_delete=models.CASCADE)

    
    mode_paiement = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.offre and self.nb_personnes:
            self.prix_total = self.offre.prix_par_personne * self.nb_personnes
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name} - {self.date_reservation}"
    
    @receiver(post_save, sender=id_reservation)
    def notify_reservation_change(sender, instance, created, **kwargs):
        if created:
            subject = "Nouvelle réservation"
            message = (
                f"Bonjour {instance.client.first_name},\n\n"
                f"Votre réservation pour '{instance.offre.titre}' a été créée avec succès.\n"
                f"Nombre de personnes : {instance.nb_personnes}\n"
                f"Prix total : {instance.prix_total}.\n"
            )
        else:
            subject = "Réservation modifiée"
            message = (
                f"Bonjour {instance.client.first_name},\n\n"
                f"Votre réservation pour '{instance.offre.titre}' a été mise à jour.\n"
                f"Nombre de personnes : {instance.nb_personnes}\n"
                f"Prix total : {instance.prix_total}.\n"
            )
        send_reservation_email(subject, message, [instance.client.email])


    @receiver(post_delete, sender=id_reservation)
    def notify_reservation_deleted(sender, instance, **kwargs):
        subject = "Réservation annulée"
        message = (
            f"Bonjour {instance.client.first_name},\n\n"
            f"Votre réservation pour '{instance.offre.titre}' a été annulée."
            )
        send_reservation_email(subject, message, [instance.client.email])
