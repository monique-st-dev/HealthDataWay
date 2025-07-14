from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.choices import UserRoles


class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.role == UserRoles.DOCTOR:
            return redirect('doctor_dashboard')
        elif request.user.role == UserRoles.PATIENT:
            return redirect('patient_dashboard')
        return redirect('home')


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/doctor_dashboard.html'


class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/patient_dashboard.html'
