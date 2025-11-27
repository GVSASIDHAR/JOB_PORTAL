from django import forms
from django.utils import timezone
from .models import Job, Application

MAX_RESUME_MB = 5

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "company_name","title", "description", "location", "job_type",
            "salary_min", "salary_max", "skills", "is_open", "deadline"
        ]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 6}),
        }

    def clean(self):
        cleaned = super().clean()
        salary_min = cleaned.get("salary_min")
        salary_max = cleaned.get("salary_max")
        deadline = cleaned.get("deadline")

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                self.add_error("salary_max", "Max salary must be greater than or equal to min salary.")

        if deadline is None:
            self.add_error("deadline", "Deadline is required.")
        else:
            if deadline < timezone.now().date():
                self.add_error("deadline", "Deadline must be today or a future date.")

        # Normalize skills
        skills = cleaned.get("skills", "")
        cleaned["skills"] = ", ".join([s.strip() for s in skills.split(",") if s.strip()])
        return cleaned
    
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "cover_letter"]
        widgets = {
            "cover_letter": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_resume(self):
        f = self.cleaned_data.get("resume")
        if not f:
            raise forms.ValidationError("Please upload your resume (PDF).")

        # Size check
        size_mb = f.size / (1024 * 1024)
        if size_mb > MAX_RESUME_MB:
            raise forms.ValidationError(f"Resume must be ≤ {MAX_RESUME_MB} MB.")

        # Content-type + magic bytes check
        ct = getattr(f, "content_type", "")
        if ct and "pdf" not in ct.lower():
            raise forms.ValidationError("Resume must be a PDF.")

        # Check PDF header (%PDF-)
        start = f.read(5)
        f.seek(0)
        if start != b"%PDF-":
            raise forms.ValidationError("Invalid PDF file.")

        return f


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status"]