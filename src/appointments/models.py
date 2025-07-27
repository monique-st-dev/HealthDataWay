from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'},
        related_name='appointments_as_doctor',
        verbose_name="Doctor",
        help_text="The doctor for this appointment.",
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='appointments_as_patient',
        verbose_name="Patient",
        help_text="The patient for this appointment.",
    )
    appointment_datetime = models.DateTimeField(
        verbose_name="Appointment Date & Time",
        help_text="The scheduled date and time of the appointment.",
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Reason for Visit",
        help_text="Optional reason or note for the appointment.",
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Confirmed",
        help_text="Indicates whether the appointment has been approved by the doctor.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date and time when the appointment was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated",
    )

    class Meta:
        ordering = ['appointment_datetime']
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        indexes = [
            models.Index(fields=["doctor"]),
            models.Index(fields=["patient"]),
            models.Index(fields=["appointment_datetime"]),
        ]


    def clean(self):
        if self.doctor_id and self.patient_id and self.doctor_id == self.patient_id:
            raise ValidationError("Doctor and patient cannot be the same person.")

    def __str__(self):
        return f"Appointment with {self.doctor.email} on {self.appointment_datetime.strftime('%Y-%m-%d %H:%M')}"
