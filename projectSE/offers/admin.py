# offers/admin.py
from django.contrib import admin
from .models import Offer, Accommodation, Flight

admin.site.register(Offer)
admin.site.register(Accommodation)
admin.site.register(Flight)
