# reservations/utils.py
from django.core.mail import send_mail

def send_reservation_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'ton_email@gmail.com',  # De
        recipient_list,         # Liste de destinataires
        fail_silently=False,
    )
