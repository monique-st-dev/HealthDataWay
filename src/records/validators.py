from django.core.exceptions import ValidationError


def validate_systolic(value):
    if not (70 <= value <= 250):
        raise ValidationError("Systolic pressure must be between 70 and 250 mmHg.")


def validate_diastolic(value):
    if not (40 <= value <= 150):
        raise ValidationError("Diastolic pressure must be between 40 and 150 mmHg.")


def validate_pulse(value):
    if not (30 <= value <= 200):
        raise ValidationError("Pulse must be between 30 and 200 bpm.")


def validate_blood_sugar(value):
    if not (2.5 <= float(value) <= 30.0):
        raise ValidationError("Blood sugar must be between 2.5 and 30.0 mmol/L.")
