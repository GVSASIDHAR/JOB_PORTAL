from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "job_type", "is_open", "deadline", "created_at")
    list_filter = ("job_type", "is_open", "deadline", "created_at")
    search_fields = ("title", "description", "location", "skills", "employer__username")