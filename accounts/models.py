# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employer", "Employer"),
        ("applicant", "Applicant"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="applicant")
    company = models.CharField(max_length=255, blank=True, null=True)  # for employers
    is_disabled = models.BooleanField(default=False)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")

    def skills_list(self):
        return [s.strip().lower() for s in self.skills.split(",") if s.strip()]