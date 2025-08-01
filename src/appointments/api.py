from rest_framework import viewsets, permissions

from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer


class IsPatientCreateAndDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            return request.user.is_authenticated and request.user.role == 'patient'
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            return obj.patient == request.user
        return True


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsPatientCreateAndDelete]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Appointment.objects.filter(patient=user).order_by('appointment_datetime')
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor=user).order_by('appointment_datetime')
        return Appointment.objects.none()

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user, is_confirmed=False)
