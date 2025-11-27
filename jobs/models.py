from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core.validators import FileExtensionValidator

class JobQuerySet(models.QuerySet):
    def open(self):
        today = timezone.now().date()
        return self.filter(is_open=True, deadline__gte=today)

class Job(models.Model):
    JOB_TYPES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
        ("remote", "Remote"),
        ("hybrid", "Hybrid"),
    )

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    company_name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default="full_time")
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    skills = models.TextField(
        blank=True,
        help_text="Comma-separated skills (e.g., Python, SQL, Django)"
    )
    is_open = models.BooleanField(default=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.employer.username}"

    def get_absolute_url(self):
        return reverse("jobs:detail", args=[self.pk])

    @property
    def is_active(self):
        return self.is_open and self.deadline >= timezone.now().date()

    def skills_list(self):
        return [s.strip().lower() for s in self.skills.split(",") if s.strip()]

class Application(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("under_review", "Under Review"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
        ("withdrawn", "Withdrawn"),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    resume = models.FileField(
        upload_to="resumes/%Y/%m/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]
        unique_together = (("job", "applicant"),)  # prevent duplicate applications

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title} ({self.status})"
    
    @property
    def display_company(self):
        return (
            self.company_name
            or getattr(self.employer, "company", "") 
            or self.employer.username
        )