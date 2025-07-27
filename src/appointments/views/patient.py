import logging
from django.utils import timezone
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from appointments.models import Appointment
from appointments.forms import AppointmentForm
from notifications.tasks import create_notification_task

logger = logging.getLogger(__name__)


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['patient'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.patient = self.request.user
        form.instance.is_confirmed = False
        response = super().form_valid(form)

        doctor = form.instance.doctor
        appt_time = form.instance.appointment_datetime.strftime("%d.%m.%Y %H:%M")

        create_notification_task.delay(
            user_id=doctor.id,
            message=f"New appointment request from {self.request.user.email} for {appt_time}.",
            notification_type="appointment_request",
        )

        logger.info(f"Appointment created by {self.request.user} for Dr. {doctor} on {appt_time}")
        messages.info(self.request, "Appointment request sent. Awaiting doctor approval.")
        return response


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(
            patient=self.request.user,
            is_confirmed=True,
            appointment_datetime__gte=timezone.now()
        ).order_by('appointment_datetime')


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')

    def test_func(self):
        return self.request.user == self.get_object().patient

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        logger.info(f"Appointment deleted by {request.user} for {appointment.appointment_datetime}")
        messages.success(request, "Appointment deleted successfully.")
        return super().delete(request, *args, **kwargs)
