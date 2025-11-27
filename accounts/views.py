from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import User

from .forms import LoginForm, SignupForm

def login_view(request):
    login_form = LoginForm(request.POST or None)
    signup_form = SignupForm()

    if request.method == "POST" and login_form.is_valid():
        username = login_form.cleaned_data["username"]
        password = login_form.cleaned_data["password"]
        role = login_form.cleaned_data["role"]

        user = authenticate(request, username=username, password=password)
        if user is None:
            login_form.add_error(None, "Invalid username or password.")
        else:
            # Admins: ignore dropdown and route straight to Django admin
            if getattr(user, "is_superuser", False) or getattr(user, "role", "") == "admin":
                login(request, user)
                return redirect("/admin/")

            # Non-admins: selected role must match stored role
            if getattr(user, "role", "") != role:
                login_form.add_error("role", "Incorrect role selected for this account.")
            else:
                login(request, user)
                if role == "employer":
                    return redirect("/dashboard/employer/")
                else:
                    return redirect("/dashboard/applicant/")

    return render(
        request,
        "accounts/auth.html",
        {
            "login_form": login_form,
            "signup_form": signup_form,
            "mode": "login",
        },
    )

def signup_view(request):
    login_form = LoginForm()
    signup_form = SignupForm(request.POST or None)

    if request.method == "POST" and signup_form.is_valid():
        user = signup_form.save()
        if user.email:
            subject = "Welcome to Job Portal"
            role = getattr(user, "role", "user")
            message = (
                f"Hi {user.username},\n\n"
                f"Your account on Job Portal has been created successfully as a '{role}'.\n\n"
                f"You can now log in and start using the platform:\n"
                f"- Applicants: browse jobs and apply.\n"
                f"- Employers: post jobs and manage applications.\n\n"
                f"Thanks,\nJob Portal Team"
            )

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception as e:
                # In a real project you would log this; for now we avoid breaking signup
                print("Error sending welcome email:", e)

        messages.success(request, "Account created. Please log in.")
        return redirect("login")

    return render(
        request,
        "accounts/auth.html",
        {
            "login_form": login_form,
            "signup_form": signup_form,
            "mode": "signup",
        },
    )

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")