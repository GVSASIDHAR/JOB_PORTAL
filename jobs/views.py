from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse, HttpResponseForbidden, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .emails import (
    send_application_submitted_email,
    send_application_status_changed_email,
)

from accounts.decorators import role_required
from .models import Job, Application
from .forms import JobForm
from .forms import ApplicationForm, ApplicationStatusForm


def job_list(request):
    qs = Job.objects.open()
    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    job_type = request.GET.get("job_type", "").strip()
    skills = request.GET.get("skills", "").strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if location:
        qs = qs.filter(location__icontains=location)
    if job_type:
        qs = qs.filter(job_type=job_type)
    if skills:
        wanted = [s.strip().lower() for s in skills.split(",") if s.strip()]
        for s in wanted:
            qs = qs.filter(skills__icontains=s)

    paginator = Paginator(qs, 10)
    page = request.GET.get("page")
    jobs = paginator.get_page(page)

    ctx = {"jobs": jobs, "q": q, "location": location, "job_type": job_type, "skills": skills}
    return render(request, "jobs/job_list.html", ctx)

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    # hide fully closed/expired job unless employer owner or admin
    if not job.is_active:
        if not request.user.is_authenticated or (not request.user.is_superuser and request.user != job.employer):
            return HttpResponseForbidden("This job is closed or expired.")
    return render(request, "jobs/job_detail.html", {"job": job})



@role_required("employer")
def employer_jobs(request):
    qs = Job.objects.filter(employer=request.user)
    paginator = Paginator(qs, 10)
    page = request.GET.get("page")
    jobs = paginator.get_page(page)
    return render(request, "jobs/employer_jobs.html", {"jobs": jobs})

@role_required("employer")
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # enforce ownership server-side
            job.save()
            messages.success(request, "Job created.")
            return redirect(job.get_absolute_url())
    else:
        form = JobForm()
    return render(request, "jobs/job_form.html", {"form": form, "mode": "create"})

@role_required("employer")
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.employer != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot edit another employer's job.")
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated.")
            return redirect(job.get_absolute_url())
    else:
        form = JobForm(instance=job)
    return render(request, "jobs/job_form.html", {"form": form, "mode": "edit", "job": job})

@role_required("applicant")
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if not job.is_active:
        return HttpResponseForbidden("This job is closed or expired.")

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, "You already applied to this job.")
        return redirect(job.get_absolute_url())

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()

            try:
                send_application_submitted_email(app)
            except Exception as e:
                print("Email failed:", e)

            messages.success(request, "Application submitted successfully.")
            return redirect("jobs:my_applications")
    else:
        form = ApplicationForm()

    return render(request, "jobs/application_form.html", {"form": form, "job": job})

@role_required("applicant")
def my_applications(request):
    apps = Application.objects.filter(applicant=request.user).select_related("job", "job__employer")
    return render(request, "jobs/my_applications.html", {"applications": apps})


@role_required("employer")
def job_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.employer != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot view applicants for another employer's job.")
    apps = job.applications.select_related("applicant")
    return render(request, "jobs/job_applicants.html", {"job": job, "applications": apps})


@login_required
def download_resume(request, app_id):
    app = get_object_or_404(Application, pk=app_id)

    
    if request.user.is_superuser or app.applicant == request.user or app.job.employer == request.user:
        if not app.resume:
            raise Http404("Resume not found.")
        return FileResponse(app.resume.open("rb"), as_attachment=True, filename=f"{app.applicant.username}_resume.pdf")
    return HttpResponseForbidden("You are not allowed to download this resume.")


@role_required("employer")
def update_application_status(request, app_id):
    app = get_object_or_404(Application, pk=app_id)

   
    if app.job.employer != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot update this application.")

    if request.method == "POST":
        form = ApplicationStatusForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            try:
                send_application_status_changed_email(app)
            except Exception as e:
                print("Email failed:", e)
            messages.success(request, "Application status updated.")
            return redirect("jobs:job_applicants", pk=app.job.pk)
    else:
        form = ApplicationStatusForm(instance=app)

    return render(request, "jobs/application_status_form.html", {"form": form, "application": app})