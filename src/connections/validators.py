from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from connections.choices import DIRECTION_VALUES, STATUS_VALUES


def validate_direction(value):
    """Ensure the direction is one of the allowed DIRECTION_CHOICES."""
    if value not in DIRECTION_VALUES:
        raise ValidationError(
            _('%(value)s is not a valid direction.'),
            params={'value': value},
        )


def validate_status(value):
    """Ensure the status is one of the allowed STATUS_CHOICES."""
    if value not in STATUS_VALUES:
        raise ValidationError(
            _('%(value)s is not a valid status.'),
            params={'value': value},
        )


def validate_different_users(doctor, patient):
    """Prevent creating a link between the same user."""
    if doctor == patient:
        raise ValidationError(_("Doctor and patient cannot be the same user."))
