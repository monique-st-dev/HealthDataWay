from django.db import models
from django.conf import settings

from connections.choices import DIRECTION_CHOICES, STATUS_CHOICES, STATUS_PENDING
from connections.validators import validate_direction, validate_status, validate_different_users


class DoctorPatientLink(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'},
        related_name='doctor_links',
        verbose_name="Doctor",
        help_text="The doctor in this doctor-patient connection.",
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='patient_links',
        verbose_name="Patient",
        help_text="The patient in this doctor-patient connection.",
    )
    direction = models.CharField(
        max_length=20,
        choices=DIRECTION_CHOICES,
        validators=[validate_direction],
        verbose_name="Medical Direction",
        help_text="Medical specialty for this doctor-patient link.",
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        validators=[validate_status],
        verbose_name="Connection Status",
        help_text="Current status of the connection.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date when the connection was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Date when the connection was last updated.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'patient', 'direction'],
                name='unique_doctor_patient_direction'
            )
        ]
        ordering = ['-created_at']
        verbose_name = "Doctor-Patient Link"
        verbose_name_plural = "Doctor-Patient Links"

    def __str__(self):
        return f"{self.patient.email} ↔ {self.doctor.email} [{self.direction}] - {self.status}"

    def clean(self):
        validate_different_users(self.doctor, self.patient)
