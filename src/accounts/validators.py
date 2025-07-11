from datetime import date, timedelta
from django.core.exceptions import ValidationError


def validate_age_over_18(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("You must be at least 18 years old to register.")
    if age > 120:
        raise ValidationError("Entered birth date seems unrealistic.")


def validate_diploma_issue_date(value):
    today = date.today()
    if value > today:
        raise ValidationError("Diploma issue date cannot be in the future.")
    if value < today - timedelta(days=80 * 365):
        raise ValidationError("Diploma issue date seems unrealistically old.")

# Optional: Email domain restriction example (use only if needed)
