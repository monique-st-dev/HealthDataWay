from django import forms
from django.utils import timezone

from .models import CardiologyRecord, EndocrinologyRecord
from .validators import validate_pulse, validate_blood_sugar


class CardiologyRecordForm(forms.ModelForm):
    class Meta:
        model = CardiologyRecord
        fields = ['systolic', 'diastolic', 'pulse', 'date', 'time', 'notes']
        widgets = {
            'systolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 120'
            }),
            'diastolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 80'
            }),
            'pulse': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 70'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'time': forms.TimeInput(format='%H:%M', attrs={
                'type': 'time',
                'step': 60,
                'class': 'form-control',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        systolic = cleaned_data.get('systolic')
        diastolic = cleaned_data.get('diastolic')
        pulse = cleaned_data.get('pulse')
        date = cleaned_data.get('date')


        if (systolic and not diastolic) or (diastolic and not systolic):
            msg = "If you fill in one of the blood (upper/lower), you must fill in the other one as well"
            self.add_error('systolic', msg)
            self.add_error('diastolic', msg)


        if systolic is not None and diastolic is not None:
            if systolic <= diastolic:
                self.add_error('systolic', "Systolic pressure must be greater than diastolic.")


        if pulse is not None:
            validate_pulse(pulse)


        if date and date > timezone.now().date():
            self.add_error('date', "Date cannot be in the future.")


class EndocrinologyRecordForm(forms.ModelForm):
    class Meta:
        model = EndocrinologyRecord
        fields = ['blood_sugar', 'date', 'time', 'notes']
        widgets = {
            'blood_sugar': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'e.g. 5.4'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'time': forms.TimeInput(format='%H:%M', attrs={
                'type': 'time',
                'step': 60,
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        blood_sugar = cleaned_data.get('blood_sugar')
        date = cleaned_data.get('date')

        if blood_sugar is not None:
            validate_blood_sugar(blood_sugar)

        if date and date > timezone.now().date():
            self.add_error('date', "Date cannot be in the future.")
