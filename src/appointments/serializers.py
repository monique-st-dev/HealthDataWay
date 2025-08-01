from rest_framework import serializers
from appointments.models import Appointment
from accounts.models import CustomUser


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = UserSummarySerializer(read_only=True)
    patient = UserSummarySerializer(read_only=True)

    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='doctor'),
        write_only=True,
        source='doctor',
    )

    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor', 'doctor_id',
            'patient',
            'appointment_datetime',
            'reason',
            'is_confirmed',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_confirmed', 'patient']
