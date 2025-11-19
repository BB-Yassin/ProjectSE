# reclamations/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class ReclamationStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'

class Reclamation(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reclamations')
    reservation = models.ForeignKey('booking.Reservation', on_delete=models.SET_NULL, null=True, blank=True, related_name='reclamations')
    type_reclamation = models.CharField(max_length=100)
    description = models.TextField()
    preuves_document = models.FileField(upload_to='reclamations/', null=True, blank=True)
    date_soumission = models.DateTimeField(auto_now_add=True)
    priorite = models.PositiveSmallIntegerField(default=3)  # 1-high ... 5-low
    status = models.CharField(max_length=20, choices=ReclamationStatus.choices, default=ReclamationStatus.OPEN)
    date_resolution = models.DateTimeField(null=True, blank=True)
    commentaire = models.TextField(blank=True)

    def resolve(self, comment=''):
        self.status = ReclamationStatus.RESOLVED
        self.date_resolution = timezone.now()
        self.commentaire = comment
        self.save()

    def __str__(self):
        return f"Reclamation #{self.id} - {self.type_reclamation} ({self.status})"
