from celery import shared_task
from django.core.mail import send_mail
from .models import Newsletter
from django.conf import settings

from_email = settings.DEFAULT_FROM_EMAIL

@shared_task
def send_newsletter(newsletter_id):
    newsletter = Newsletter.objects.get(id=newsletter_id)
    recipients = newsletter.recipients.split(',')
    send_mail(
        newsletter.subject,
        newsletter.message,
        from_email,
        recipients,
        fail_silently=False,
    )