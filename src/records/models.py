from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime

from accounts.models import CustomUser
from records.validators import validate_pulse, validate_blood_sugar

from django.utils.timezone import localtime

def get_current_time():
    return localtime().time()

class DirectionType(models.Model):
    """
    Represents a medical direction: Cardiology, Endocrinology
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Direction Name",
        help_text="Full name of the medical direction (e.g., Cardiology).",
    )
    code = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Direction Code",
        help_text="URL-friendly identifier for the direction.",
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Direction"
        verbose_name_plural = "Directions"

    def __str__(self):
        return self.name


class CardiologyRecord(models.Model):
    """
    A record for cardiology: blood pressure and pulse
    """
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='cardiology_records',
        verbose_name="Patient",
        help_text="The patient to whom this cardiology record belongs.",
    )
    systolic = models.PositiveSmallIntegerField(
        help_text="Systolic pressure (upper value in mmHg).",
        verbose_name="Systolic Pressure",
        blank=True,
        null=True,
    )
    diastolic = models.PositiveSmallIntegerField(
        help_text="Diastolic pressure (lower value in mmHg).",
        verbose_name="Diastolic Pressure",
        blank=True,
        null=True,
    )
    pulse = models.PositiveSmallIntegerField(
        help_text="Pulse in beats per minute (bpm).",
        verbose_name="Pulse (bpm)",
        validators=[validate_pulse],
        blank=True,
        null=True,
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="Date",
        help_text="Date of the measurement.",
    )
    time = models.TimeField(
        default=get_current_time,
        verbose_name="Time",
        help_text="Time of the measurement.",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
        help_text="Optional notes for this cardiology record.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date and time when the record was created.",
    )

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Cardiology Record"
        verbose_name_plural = "Cardiology Records"

    def __str__(self):
        return f"{self.patient.email} – BP: {self.systolic}/{self.diastolic}, Pulse: {self.pulse}"

    def clean(self):
        if self.systolic is not None and self.diastolic is not None:
            if self.systolic <= self.diastolic:
                raise ValidationError("Systolic pressure must be greater than diastolic pressure.")
            if not (70 <= self.systolic <= 250):
                raise ValidationError("Systolic pressure must be between 70 and 250 mmHg.")
            if not (40 <= self.diastolic <= 150):
                raise ValidationError("Diastolic pressure must be between 40 and 150 mmHg.")


class EndocrinologyRecord(models.Model):
    """
    Stores blood sugar data for a specific patient.
    """
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='endocrinology_records',
        verbose_name="Patient",
        help_text="The patient to whom this endocrinology record belongs.",
    )
    blood_sugar = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Blood Sugar",
        help_text="Blood sugar level in mmol/L.",
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="Date",
        help_text="Date of the measurement.",
    )
    time = models.TimeField(
        default=get_current_time,
        verbose_name="Time",
        help_text="Time of the measurement.",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
        help_text="Optional notes for this endocrinology record.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date and time when the record was created.",
    )

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Endocrinology Record"
        verbose_name_plural = "Endocrinology Records"

    def __str__(self):
        return f"{self.patient.email} – Blood Sugar: {self.blood_sugar} mmol/L"

    def clean(self):
        if self.blood_sugar < 2.5 or self.blood_sugar > 30.0:
            raise ValidationError({'blood_sugar': "Blood sugar must be between 2.5 and 30.0 mmol/L."})
