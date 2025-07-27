from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from connections.models import DoctorPatientLink
from connections.choices import (
    STATUS_PENDING, STATUS_APPROVED, STATUS_DECLINED, STATUS_CANCELLED_BY_PATIENT
)


class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'patient'


class PatientConnectionRequestsView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    template_name = 'connections/patient_requests.html'
    context_object_name = 'requests'
    model = DoctorPatientLink

    def get_queryset(self):
        return DoctorPatientLink.objects.filter(
            patient=self.request.user,
            status=STATUS_PENDING
        )


class PatientRespondView(LoginRequiredMixin, PatientRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        link_id = kwargs.get('pk')
        action = request.POST.get('action')

        link = get_object_or_404(
            DoctorPatientLink,
            id=link_id,
            patient=request.user,
            status=STATUS_PENDING,
        )

        if action == 'approve':
            link.status = STATUS_APPROVED
            messages.success(
                request,
                _(f"You approved the connection with Dr. {link.doctor.email}.")
            )
        elif action == 'decline':
            link.status = STATUS_DECLINED
            messages.info(
                request,
                _(f"You declined the connection with Dr. {link.doctor.email}.")
            )
        else:
            messages.error(request, _("Invalid action submitted."))

        link.save()
        return redirect(reverse('patient-connections'))


class PatientConnectionsView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    template_name = 'connections/patient_connections.html'
    context_object_name = 'connections'
    model = DoctorPatientLink

    def get_queryset(self):
        return DoctorPatientLink.objects.filter(
            patient=self.request.user,
            status=STATUS_APPROVED
        ).select_related('doctor')


class PatientDisconnectView(LoginRequiredMixin, PatientRequiredMixin, View):
    def post(self, request, pk):
        link = get_object_or_404(
            DoctorPatientLink,
            pk=pk,
            patient=request.user,
            status=STATUS_APPROVED
        )
        link.status = STATUS_CANCELLED_BY_PATIENT
        link.save()
        messages.success(request, _(f"You disconnected from Dr. {link.doctor.email}."))
        return redirect('patient-connections')
