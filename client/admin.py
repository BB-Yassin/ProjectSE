
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Your custom User model

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Optional: Customize fields display (e.g., show email, fullname, role)
    list_display = ('username', 'email', 'first_name', 'last_name', 'fullname', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')  # Filters for easy searching
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Search bar
    # Add other customizations if needed (e.g., readonly_fields)