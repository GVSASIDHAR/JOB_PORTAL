# accounts/admin.py
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_disabled")
    list_filter = ("role", "is_active", "is_disabled")
    search_fields = ("username", "email")