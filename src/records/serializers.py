from rest_framework import serializers
from .models import EndocrinologyRecord, CardiologyRecord
from datetime import datetime


class EndocrinologyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndocrinologyRecord
        fields = '__all__'
        read_only_fields = ['patient']

    def validate_time(self, value):
        if isinstance(value, datetime):
            return value.time()
        return value


class CardiologyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardiologyRecord
        fields = '__all__'
        read_only_fields = ['patient']
