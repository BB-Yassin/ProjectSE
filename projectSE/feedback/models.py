# feedback/models.py
from django.db import models
from django.conf import settings

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='feedbacks')
    reservation = models.ForeignKey('booking.Reservation', on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    note = models.PositiveSmallIntegerField(null=True, blank=True)  # rating 1..5
    date_soumission = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    attachement = models.FileField(upload_to='feedback_attachments/', null=True, blank=True)

    def __str__(self):
        return f"Feedback #{self.id} by {self.user.get_full_name() if self.user else 'Anonymous'}"
