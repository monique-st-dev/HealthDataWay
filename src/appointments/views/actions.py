from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib import messages
import logging

from appointments.models import Appointment
from notifications.tasks import create_notification_task

logger = logging.getLogger(__name__)


@method_decorator(require_POST, name='dispatch')
class ApproveAppointmentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'doctor'

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        if appointment.doctor != request.user:
            logger.warning(f"Unauthorized approval attempt by {request.user} for appointment {pk}")
            return HttpResponseForbidden("You are not allowed to approve this appointment.")

        appointment.is_confirmed = True
        appointment.save()

        try:
            create_notification_task.delay(
                user_id=appointment.patient.id,
                message=f"Your appointment on {appointment.appointment_datetime.strftime('%d.%m.%Y %H:%M')} was approved.",
                notification_type="appointment_approved",
            )
            logger.info(f"Appointment {pk} approved by doctor {request.user}")
        except Exception as e:
            logger.error(f"Failed to send approval notification for appointment {pk}: {e}")

        messages.success(request, "Appointment approved.")
        return redirect(reverse('doctor_appointment_list'))


@method_decorator(require_POST, name='dispatch')
class RejectAppointmentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'doctor'

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        if appointment.doctor != request.user:
            logger.warning(f"Unauthorized rejection attempt by {request.user} for appointment {pk}")
            return HttpResponseForbidden("You are not allowed to reject this appointment.")

        patient_id = appointment.patient.id
        appt_time = appointment.appointment_datetime.strftime('%d.%m.%Y %H:%M')
        appointment.delete()

        try:
            create_notification_task.delay(
                user_id=patient_id,
                message=f"Your appointment on {appt_time} was rejected.",
                notification_type="appointment_rejected",
            )
            logger.info(f"Appointment {pk} rejected and deleted by doctor {request.user}")
        except Exception as e:
            logger.error(f"Failed to send rejection notification for appointment {pk}: {e}")

        messages.warning(request, "Appointment rejected and deleted.")
        return redirect(reverse('doctor_appointment_list'))

@method_decorator(require_POST, name='dispatch')
class CancelConfirmedAppointmentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk, is_confirmed=True)

        if request.user == appointment.doctor:
            recipient = appointment.patient
            canceled_by = 'doctor'
            redirect_url = 'doctor_appointment_list'
        elif request.user == appointment.patient:
            recipient = appointment.doctor
            canceled_by = 'patient'
            redirect_url = 'appointment_list'
        else:
            return HttpResponseForbidden("You are not allowed to cancel this appointment.")

        appt_time = appointment.appointment_datetime.strftime('%d.%m.%Y %H:%M')
        appointment.delete()

        create_notification_task.delay(
            user_id=recipient.id,
            message=f"Your confirmed appointment on {appt_time} was cancelled by the {canceled_by}.",
            notification_type="appointment_cancelled",
        )


        messages.warning(request, "Confirmed appointment cancelled.")
        return redirect(reverse(redirect_url))
