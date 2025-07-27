from datetime import date, timedelta
from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext as _


def validate_age_over_18(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("You must be at least 18 years old to register.")
    if age > 120:
        raise ValidationError("Entered birth date seems unrealistic.")


def validate_phone_number(value):
    if not re.match(r'^\+?\d{7,15}$', value):
        raise ValidationError("Enter a valid phone number (7 to 15 digits, optional + at the start).")



class NoReuseOldPasswordValidator:
    def validate(self, password, user=None):
        if user and user.check_password(password):
            raise ValidationError(
                _("The new password cannot be the same as your current password."),
                code='password_no_reuse',
            )

    def get_help_text(self):
        return _("Your new password cannot be the same as your current password.")