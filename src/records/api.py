from rest_framework import viewsets, permissions
from .models import EndocrinologyRecord, CardiologyRecord
from .serializers import EndocrinologyRecordSerializer, CardiologyRecordSerializer

class EndocrinologyRecordViewSet(viewsets.ModelViewSet):
    serializer_class = EndocrinologyRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EndocrinologyRecord.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class CardiologyRecordViewSet(viewsets.ModelViewSet):
    serializer_class = CardiologyRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CardiologyRecord.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
