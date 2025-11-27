# accounts/forms.py
from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import User

ROLE_CHOICES = [
    ("applicant", "Applicant"),
    ("employer", "Employer"),
    ("admin", "Admin"),
]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    admin_code = forms.CharField(
        required=False,
        help_text="Required only if you choose Admin.",
        widget=forms.PasswordInput(render_value=False),
        label="Admin Invite Code",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "role", "company", "summary", "skills", "admin_code"]

    def clean_role(self):
        role = self.cleaned_data["role"]
        if role not in {"applicant", "employer", "admin"}:
            raise forms.ValidationError("Invalid role.")
        # default: allow admin signup in dev; set ALLOW_ADMIN_SIGNUP=0 in prod
        allow = getattr(settings, "ALLOW_ADMIN_SIGNUP", True)
        if role == "admin" and not allow:
            raise forms.ValidationError("Admin signup is disabled.")
        return role

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        company = cleaned.get("company")
        summary = cleaned.get("summary")
        skills = cleaned.get("skills")
        admin_code = cleaned.get("admin_code")

        if role == "employer" and not company:
            self.add_error("company", "Company name is required for employer accounts.")
        if role == "applicant":
            if not summary:
                self.add_error("summary", "Profile summary is required for applicants.")
            if not skills:
                self.add_error("skills", "Skills are required for applicants.")
        if role == "admin":
            invite = getattr(settings, "ADMIN_INVITE_CODE", "LETMEIN")
            if not admin_code:
                self.add_error("admin_code", "Admin invite code is required.")
            elif admin_code != invite:
                self.add_error("admin_code", "Invalid admin invite code.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        # hash password
        user.password = make_password(self.cleaned_data["password"])

        role = self.cleaned_data["role"]
        # sanitize irrelevant fields and set flags
        if role == "admin":
            user.role = "admin"
            user.is_staff = True
            user.is_superuser = True
            user.company = ""
            user.summary = ""
            user.skills = ""
        elif role == "employer":
            user.summary = ""
            user.skills = ""
        elif role == "applicant":
            user.company = ""

        if commit:
            user.save()
        return user