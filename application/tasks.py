from time import sleep
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from application.models import Application
from django.utils.timezone import now

       
@shared_task
def send_application_email(applicant_email, subject, message):
    send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [applicant_email],
            fail_silently=False
        )


@shared_task
def update_applications_after_event():
    today = now().date()
    
    applications = Application.objects.filter(event__event_type='gig').filter(event__date__lt=today)

    applications.update(status="performed")

