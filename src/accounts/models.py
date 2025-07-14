from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from accounts.choices import UserRoles, GenderChoices
from accounts.managers import CustomUserManager
from accounts.validators import validate_age_over_18, validate_diploma_issue_date


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(
        unique=True,
        verbose_name="Email address",
        help_text="Enter a valid email address. Used for login.",
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date joined",
        help_text="The date and time when the account was created.",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this account is active.",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff status",
        help_text="Designates whether the user can access the admin site.",
    )

    role = models.CharField(
        max_length=10,
        choices=UserRoles.CHOICES,
        default=UserRoles.PATIENT,
        verbose_name="Role",
        help_text="Defines the user's role: patient, doctor, staff or admin.",
    )

    objects = CustomUserManager()

    def is_patient(self):
        return self.role == UserRoles.PATIENT

    def is_doctor(self):
        return self.role == UserRoles.DOCTOR

    def is_staff_user(self):
        return self.role == UserRoles.STAFF

    def is_admin(self):
        return self.role == UserRoles.ADMIN

    def __str__(self):
        return f"{self.email} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="The user this profile belongs to.",
    )
    full_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Full name",
        help_text="Enter your full name.",
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of Birth",
        help_text="Enter your birth date (must be at least 18 years old).",
        validators=[validate_age_over_18],
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.CHOICES,
        blank=True,
        verbose_name="Gender",
        help_text="Select your gender (optional).",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone number",
        help_text="Optional contact number.",
    )
    image = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name="Profile picture",
        help_text="Optional profile image.",
    )

    def __str__(self):
        return f"Profile of {self.user.email}"


class DoctorData(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Doctor",
        help_text="The doctor this data belongs to.",
    )
    diploma_number = models.CharField(
        max_length=50,
        verbose_name="Diploma number",
        help_text="Official diploma number.",
    )
    diploma_issue_date = models.DateField(
        verbose_name="Diploma issue date",
        help_text="Date when the diploma was issued.",
        validators=[validate_diploma_issue_date],
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specialization",
        help_text="Medical specialization, e.g. Cardiology (optional).",
    )

    def __str__(self):
        return f"Dr. {self.user.email} – {self.diploma_number}"


class DoctorPatientLink(models.Model):
    doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='linked_patients',
        verbose_name="Doctor",
        help_text="The doctor in this relationship.",
        limit_choices_to={'role': UserRoles.DOCTOR},
    )
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='linked_doctors',
        verbose_name="Patient",
        help_text="The patient in this relationship.",
        limit_choices_to={'role': UserRoles.PATIENT},
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date linked",
        help_text="Date and time when the doctor–patient relationship was created.",
    )

    class Meta:
        unique_together = ('doctor', 'patient')
        verbose_name = "Doctor–Patient Link"
        verbose_name_plural = "Doctor–Patient Links"

    def __str__(self):
        return f"{self.doctor.email} ↔ {self.patient.email}"
