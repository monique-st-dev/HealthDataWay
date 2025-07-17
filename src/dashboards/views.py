from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.choices import UserRoles
import logging
logger = logging.getLogger(__name__)

class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.role == UserRoles.DOCTOR:
            return redirect('doctor_dashboard')
        elif request.user.role == UserRoles.PATIENT:
            return redirect('patient_dashboard')
        return redirect('home')


class DoctorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboards/doctor_dashboard.html'

    def test_func(self):
        return self.request.user.role == UserRoles.DOCTOR


class PatientDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboards/patient_dashboard.html'

    def test_func(self):
        return self.request.user.role == UserRoles.PATIENT
