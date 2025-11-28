from django.db import models
from django.db import models


class Destination(models.Model):
    nom_destination = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    description = models.TextField()
    saison = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="destinations/")

    def __str__(self):
        return f"{self.nom_destination} ({self.pays})"

class Offer(models.Model):
    titre = models.CharField(max_length=150)
    description = models.TextField()
    nom_destinations = models.ManyToManyField(Destination)
    prix_par_personne = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="offres/",default="offres/default.jpg")
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.titre
