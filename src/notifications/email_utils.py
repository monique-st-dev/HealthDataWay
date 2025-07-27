import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_connection_notification_task(to_email, subject, message, html_message=None):
    if not to_email:
        logger.warning("No recipient email provided for notification.")
        return

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        if html_message:
            email.attach_alternative(html_message, "text/html")

        email.send()
        logger.info(f"Email sent to {to_email} with subject '{subject}'")

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
