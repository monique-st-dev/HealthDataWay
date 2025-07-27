from django.contrib import admin
from appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient_email',
        'doctor_email',
        'appointment_datetime',
        'is_confirmed',
        'created_at',
    )
    list_filter = ('is_confirmed', 'appointment_datetime', 'created_at')
    search_fields = ('patient__email', 'doctor__email', 'reason')
    ordering = ('-appointment_datetime',)
    date_hierarchy = 'appointment_datetime'
    readonly_fields = ('created_at',)

    def patient_email(self, obj):
        return obj.patient.email
    patient_email.short_description = 'Patient Email'

    def doctor_email(self, obj):
        return obj.doctor.email
    doctor_email.short_description = 'Doctor Email'
