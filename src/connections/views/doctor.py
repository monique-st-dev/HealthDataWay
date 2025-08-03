from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, View, DetailView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from charts.forms import ChartFilterForm
from connections.forms import DoctorAddPatientForm
from connections.models import DoctorPatientLink
from connections.choices import (
    STATUS_PENDING, STATUS_APPROVED, STATUS_CANCELLED_BY_DOCTOR
)
from records.models import CardiologyRecord, EndocrinologyRecord


class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'doctor'


class DoctorCreateLinkView(LoginRequiredMixin, DoctorRequiredMixin, FormView):
    template_name = 'connections/doctor_add_patient.html'
    form_class = DoctorAddPatientForm
    success_url = reverse_lazy('doctor-patients-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['doctor'] = self.request.user
        return kwargs

    def form_valid(self, form):
        patient = form.cleaned_data['patient']
        direction = form.cleaned_data['direction']

        try:
            link = DoctorPatientLink.objects.get(
                doctor=self.request.user,
                patient=patient,
                direction=direction
            )
            link.status = STATUS_PENDING
            link.save()
            messages.info(self.request, _(f"A new request was sent again to {patient.email} ({direction})."))
        except DoctorPatientLink.DoesNotExist:
            DoctorPatientLink.objects.create(
                doctor=self.request.user,
                patient=patient,
                direction=direction,
                status=STATUS_PENDING,
            )
            messages.success(self.request, _(f"Request sent to {patient.email} ({direction})."))

        from notifications.tasks import create_notification_task
        from notifications.notification_constants import CONNECTION_REQUEST

        create_notification_task.delay(
            user_id=patient.id,
            notification_type=CONNECTION_REQUEST,
            message=f"You have a new connection request from Dr. {self.request.user.profile.full_name or self.request.user.email}"
        )


        return redirect(self.get_success_url())



class DoctorPatientsListView(LoginRequiredMixin, DoctorRequiredMixin, ListView):
    template_name = 'connections/doctor_patients_list.html'
    context_object_name = 'links'
    model = DoctorPatientLink

    def get_queryset(self):
        return DoctorPatientLink.objects.filter(
            doctor=self.request.user,
            status__in=[STATUS_PENDING, STATUS_APPROVED],
        ).select_related('patient').order_by('direction', 'status')


class DoctorCancelLinkView(LoginRequiredMixin, DoctorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        link_id = kwargs.get('pk')
        link = get_object_or_404(
            DoctorPatientLink,
            id=link_id,
            doctor=request.user,
            status=STATUS_APPROVED,
        )

        link.status = STATUS_CANCELLED_BY_DOCTOR
        link.save()

        messages.info(
            request,
            _(f"You have cancelled the connection with patient {link.patient.email}.")
        )
        return redirect(reverse('doctor-patients-list'))


class DoctorPatientDetailView(LoginRequiredMixin, DoctorRequiredMixin, DetailView):
    template_name = 'connections/doctor_patient_detail.html'
    model = CustomUser
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user
        patient = self.get_object()

        from django.core.exceptions import PermissionDenied
        try:
            link = DoctorPatientLink.objects.get(
                doctor=doctor,
                patient=patient,
                status=STATUS_APPROVED
            )
        except DoctorPatientLink.DoesNotExist:
            raise PermissionDenied("You do not have permission to view this patient's data.")

        direction = link.direction

        direction_models = {
            'cardiology': CardiologyRecord,
            'endocrinology': EndocrinologyRecord,
        }

        model = direction_models.get(direction)
        if model:
            context[f'{direction}_records'] = model.objects.filter(patient=patient)

        context['direction'] = direction
        return context


class DoctorPatientReportView(LoginRequiredMixin, DoctorRequiredMixin, DetailView):
    template_name = 'connections/doctor_patient_report.html'
    model = CustomUser
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user
        patient = self.get_object()

        try:
            link = DoctorPatientLink.objects.get(
                doctor=doctor,
                patient=patient,
                status=STATUS_APPROVED
            )
        except DoctorPatientLink.DoesNotExist:
            raise PermissionDenied("You do not have permission to view this patient's report.")

        direction = link.direction
        context['direction'] = direction

        form = ChartFilterForm(self.request.GET or None)
        context['form'] = form

        if form.is_valid():
            period_type = form.cleaned_data['period_type']
            selected_date = form.cleaned_data['selected_date']
            metrics = form.cleaned_data['metrics']

            # период
            if period_type == 'day':
                start_date = end_date = selected_date
            elif period_type == 'week':
                start_date = selected_date
                end_date = start_date + timedelta(days=6)
            elif period_type == 'month':
                start_date = selected_date.replace(day=1)
                if selected_date.month == 12:
                    end_date = selected_date.replace(year=selected_date.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    end_date = selected_date.replace(month=selected_date.month + 1, day=1) - timedelta(days=1)

            context['start_date'] = start_date
            context['end_date'] = end_date
            context['metrics'] = metrics

            if direction == 'cardiology':
                cardio_data = CardiologyRecord.objects.filter(
                    patient=patient,
                    date__range=(start_date, end_date),
                )

                if 'pressure' in metrics and 'pulse' not in metrics:
                    cardio_data = cardio_data.exclude(systolic__isnull=True, diastolic__isnull=True)
                elif 'pulse' in metrics and 'pressure' not in metrics:
                    cardio_data = cardio_data.exclude(pulse__isnull=True)
                elif 'pulse' in metrics and 'pressure' in metrics:
                    cardio_data = cardio_data.exclude(
                        systolic__isnull=True,
                        diastolic__isnull=True,
                        pulse__isnull=True,
                    )

                context['cardio_data'] = cardio_data.order_by('date')

            elif direction == 'endocrinology':
                if 'sugar' in metrics:
                    sugar_data = EndocrinologyRecord.objects.filter(
                        patient=patient,
                        date__range=(start_date, end_date),
                    ).order_by('date')
                    context['sugar_data'] = sugar_data

        return context
