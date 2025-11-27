# jobs/emails.py
from django.core.mail import send_mail
from django.conf import settings

def _safe_send_mail(subject: str, message: str, recipient_list: list[str]) -> None:
    """
    Wrapper around send_mail that skips empty emails and fails silently.
    """
    recipient_list = [e for e in recipient_list if e]
    if not recipient_list:
        return

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@jobportal.local")

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=True,  # in dev we don't want crashes on email issues
    )


def send_application_submitted_email(application) -> None:
    """Notify the employer and confirm to the applicant when a new application is submitted."""
    job = application.job
    employer = job.employer
    applicant = application.applicant

    # Email to employer
    subject_employer = f"New application for '{job.title}'"
    message_employer = (
        f"Hello {employer.username},\n\n"
        f"You have received a new application for your job posting:\n"
        f"Title: {job.title}\n"
        f"Applicant: {applicant.username}\n"
        f"Status: {application.get_status_display()}\n\n"
        f"Log in to your dashboard to review the application.\n\n"
        f"- Job Portal"
    )

    _safe_send_mail(subject_employer, message_employer, [employer.email])

    # Confirmation email to applicant
    subject_applicant = f"Application received for '{job.title}'"
    message_applicant = (
        f"Hello {applicant.username},\n\n"
        f"We have received your application for the job '{job.title}' at {getattr(job, 'company_name', 'the employer')}.\n"
        f"Current status: {application.get_status_display()}.\n\n"
        f"You can log in to your dashboard at any time to track the progress of your application.\n\n"
        f"- Job Portal"
    )

    _safe_send_mail(subject_applicant, message_applicant, [applicant.email])


def send_application_status_changed_email(application) -> None:
    """
    Notify the applicant that their application status has changed.
    """
    job = application.job
    applicant = application.applicant

    subject = f"Your application status for '{job.title}' has changed"
    message = (
        f"Hello {applicant.username},\n\n"
        f"The status of your application for the job '{job.title}' has been updated.\n"
        f"New status: {application.get_status_display()}\n\n"
        f"Log in to your dashboard to see more details.\n\n"
        f"- Job Portal"
    )

    _safe_send_mail(subject, message, [applicant.email])