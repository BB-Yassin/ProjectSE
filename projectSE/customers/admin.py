# customers/admin.py
from django.contrib import admin
from .models import CustomerInfo, GuestUser

admin.site.register(CustomerInfo)
admin.site.register(GuestUser)
