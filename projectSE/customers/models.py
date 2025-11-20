# customers/models.py
from django.db import models
from django.conf import settings

class CustomerInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_info')
    civilite = models.CharField(max_length=20, blank=True)  # Mr/Ms/etc
    numero_passport = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)
    numero_telephone = models.CharField(max_length=50, blank=True, null=True)
    numero_c_identite = models.CharField("ID Number", max_length=100, blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True)
    nom = models.CharField(max_length=80, blank=True, null=True)
    prenom = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return f"CustomerInfo for {self.user.get_full_name()}"

class GuestUser(models.Model):
    session = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GuestUser {self.session}"
