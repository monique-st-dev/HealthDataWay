from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from accounts.choices import UserRoles
from connections.models import DoctorPatientLink
from connections.choices import STATUS_PENDING, STATUS_APPROVED
from appointments.models import Appointment
from notifications.models import Notification

import logging
logger = logging.getLogger(__name__)


class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == UserRoles.DOCTOR:
            logger.debug(f"Redirecting doctor {user.email} to dashboard.")
            return redirect('doctor_dashboard')
        elif user.role == UserRoles.PATIENT:
            logger.debug(f"Redirecting patient {user.email} to dashboard.")
            return redirect('patient_dashboard')
        logger.warning(f"Unknown role for user {user.email}, redirecting to home.")
        return redirect('home')


class DoctorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboards/doctor_dashboard.html'

    def test_func(self):
        return self.request.user.role == UserRoles.DOCTOR

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['active_count'] = DoctorPatientLink.objects.filter(
            doctor=user, status=STATUS_APPROVED
        ).count()

        context['pending_count'] = DoctorPatientLink.objects.filter(
            doctor=user, status=STATUS_PENDING
        ).count()

        context['approved_connections'] = DoctorPatientLink.objects.filter(
            doctor=user, status=STATUS_APPROVED
        ).select_related('patient')

        context['upcoming_appointments'] = Appointment.objects.filter(
            doctor=user,
            is_confirmed=True,
            appointment_datetime__gte=timezone.now()
        ).order_by('appointment_datetime')[:5]

        context['unread_notifications'] = Notification.objects.filter(
            recipient=user,
            is_read=False
        ).order_by('-created_at')[:5]

        return context


class PatientDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboards/patient_dashboard.html'

    def test_func(self):
        return self.request.user.role == UserRoles.PATIENT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        unread_notifications = Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).order_by('-created_at')



        context['unread_notifications'] = unread_notifications[:5]


        context['upcoming_appointments'] = Appointment.objects.filter(
            patient=self.request.user,
            appointment_datetime__gte=timezone.now(),
            is_confirmed=True
        ).order_by('appointment_datetime')[:5]


        context['connections'] = DoctorPatientLink.objects.filter(
            patient=self.request.user,
            status=STATUS_APPROVED
        ).select_related('doctor')

        return context
