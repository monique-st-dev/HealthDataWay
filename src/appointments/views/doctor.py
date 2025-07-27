from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from appointments.models import Appointment


class DoctorAppointmentListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'appointments/doctor_appointment_list.html'

    def test_func(self):
        return self.request.user.role == 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user
        now = timezone.now()

        context['confirmed_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            is_confirmed=True,
            appointment_datetime__gte=now
        ).order_by('appointment_datetime')

        context['pending_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            is_confirmed=False,
            appointment_datetime__gte=now
        ).order_by('appointment_datetime')

        return context
