from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class Roles(models.TextChoices):
    CLIENT =     'CLIENT', _('Client')      # Registered client (can manage reservations)
    ADMIN =      'ADMIN', _('Admin')        # Site administrator (full access)  
class User(AbstractUser):
  first_name = models.CharField(max_length=30, blank=False)
  last_name = models.CharField(max_length=30, blank=False)
  email = models.EmailField(unique=True, blank=False)
  role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.CLIENT,
    )
  created_at = models.DateTimeField(auto_now_add=True)
  address = models.CharField(max_length=255, blank=True, null=True)
  phone_number = models.CharField(max_length=20, blank=True, null=True)

  # Make email the login field instead of username
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  
  def clean(self):
        super().clean()
        # Check for duplicate email, excluding current instance
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': _('A user with this email already exists.')})
        
def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')