from django.contrib import admin
from connections.models import DoctorPatientLink
from connections.choices import DIRECTION_CHOICES, STATUS_CHOICES


@admin.register(DoctorPatientLink)
class DoctorPatientLinkAdmin(admin.ModelAdmin):
    model = DoctorPatientLink

    list_display = (
        'doctor_display',
        'patient_display',
        'direction',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'direction',
        'created_at',
    )
    search_fields = (
        'doctor__email',
        'patient__email',
    )
    ordering = ('-created_at',)
    autocomplete_fields = ['doctor', 'patient']
    readonly_fields = ('created_at', 'updated_at')

    def doctor_display(self, obj):
        return obj.doctor.email
    doctor_display.short_description = 'Doctor Email'

    def patient_display(self, obj):
        return obj.patient.email
    patient_display.short_description = 'Patient Email'
