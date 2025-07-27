from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from connections.models import DoctorPatientLink
from connections.choices import DIRECTION_CHOICES, STATUS_APPROVED, STATUS_PENDING

User = get_user_model()


class DoctorAddPatientForm(forms.Form):
    patient_email = forms.EmailField(
        label="Patient Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter patient email'}),
    )
    direction = forms.ChoiceField(
        label="Direction",
        choices=DIRECTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, doctor: User = None, **kwargs):
        if doctor is None:
            raise ValueError("Doctor must be provided to DoctorAddPatientForm")
        self.doctor = doctor
        super().__init__(*args, **kwargs)

    def clean_patient_email(self):
        email = self.cleaned_data['patient_email']
        try:
            patient = User.objects.get(email=email, role='patient')
        except User.DoesNotExist:
            raise ValidationError("No patient with this email was found or the user is not registered as a patient.")
        self.cleaned_data['patient'] = patient
        return email

    def clean(self):
        cleaned_data = super().clean()
        patient = cleaned_data.get('patient')
        direction = cleaned_data.get('direction')

        if not patient or not direction:
            return

        existing = DoctorPatientLink.objects.filter(
            doctor=self.doctor,
            patient=patient,
            direction=direction,
            status__in=[STATUS_PENDING, STATUS_APPROVED],
        ).exists()

        if existing:
            raise ValidationError(
                f"You already have an active or pending connection with {patient.email} for {direction}."
            )

        return cleaned_data
