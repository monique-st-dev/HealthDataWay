from datetime import timedelta
import logging

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils import timezone

from appointments.models import Appointment
from .models import Notification
from .notification_constants import NOTIFICATION_TYPES

logger = logging.getLogger(__name__)


@shared_task
def create_notification_task(user_id, message, notification_type='reminder'):
    User = get_user_model()
    try:
        recipient = User.objects.get(id=user_id)

        if recipient.role not in ['doctor', 'patient']:
            logger.warning(f"Invalid role for user {user_id}. Notification not created.")
            return None

        valid_types = [key for key, _ in NOTIFICATION_TYPES]
        if notification_type not in valid_types:
            logger.warning(f"Invalid notification type '{notification_type}' for user {user_id}.")
            return None


        Notification.objects.create(
            recipient=recipient,
            message=message,
            notification_type=notification_type,
            is_read=False,
        )
        logger.info(f"Notification created for user {user_id}")
        return f"Notification created for user {user_id}"

    except ObjectDoesNotExist:
        logger.warning(f"User with id {user_id} not found for notification.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in create_notification_task: {e}")
        return None


# @shared_task
# def send_appointment_reminders():
#     now = timezone.now()
#     target_time = now + timedelta(hours=24)
#     window_start = target_time - timedelta(minutes=5)
#     window_end = target_time + timedelta(minutes=5)
#
#     upcoming_appointments = Appointment.objects.select_related('doctor', 'patient').filter(
#         is_confirmed=True,
#         appointment_datetime__range=(window_start, window_end),
#     )
#
#     for appt in upcoming_appointments:
#         try:
#             patient = appt.patient
#             doctor = appt.doctor
#             time_str = appt.appointment_datetime.strftime('%d.%m.%Y at %H:%M')
#
#             create_notification_task.delay(
#                 user_id=patient.id,
#                 message=f"Reminder: You have an appointment with Dr. {doctor.email} on {time_str}",
#                 notification_type='appointment_reminder'
#             )
#
#         except Exception as e:
#             logger.error(f"Error sending reminder for appointment {appt.id}: {e}")
