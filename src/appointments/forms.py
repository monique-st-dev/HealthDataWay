from django import forms
from django.db.models import Subquery
from django.utils import timezone

from accounts.models import CustomUser
from appointments.models import Appointment
from connections.models import DoctorPatientLink


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_datetime', 'reason']
        widgets = {
            'appointment_datetime': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'reason': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Optional reason for the appointment',
            }),
        }
        labels = {
            'doctor': 'Select Doctor',
            'appointment_datetime': 'Appointment Date & Time',
            'reason': 'Reason (optional)',
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)

        if self.patient:
            approved_links = DoctorPatientLink.objects.filter(
                patient=self.patient,
                status='approved'
            )

            self.fields['doctor'].queryset = CustomUser.objects.filter(
                id__in=Subquery(approved_links.values('doctor_id'))
            )
            self.fields['doctor'].widget.attrs.update({'class': 'form-select'})

    def clean_appointment_datetime(self):
        date = self.cleaned_data['appointment_datetime']
        if date < timezone.now():
            raise forms.ValidationError("Appointment date must be in the future.")
        return date
