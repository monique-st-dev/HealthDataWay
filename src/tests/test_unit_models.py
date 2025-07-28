import pytest
from django.utils import timezone

from accounts.models import CustomUser
from notifications.models import Notification
from connections.models import DoctorPatientLink
from connections.choices import STATUS_APPROVED


@pytest.mark.django_db
def test_mark_as_read_method_sets_flag_and_saves():
    user = CustomUser.objects.create_user(email='user@test.com', password='pass', role='patient')
    notification = Notification.objects.create(
        recipient=user,
        message="Test Message",
        notification_type='reminder',
        created_at=timezone.now(),
        is_read=False,
    )

    # Act
    notification.mark_as_read()

    # Assert
    assert notification.is_read is True


@pytest.mark.django_db
def test_doctor_patient_str_method_returns_correct_format():
    doctor = CustomUser.objects.create_user(email='doc@test.com', password='pass', role='doctor')
    patient = CustomUser.objects.create_user(email='pat@test.com', password='pass', role='patient')

    link = DoctorPatientLink.objects.create(
        doctor=doctor,
        patient=patient,
        direction='cardiology',
        status=STATUS_APPROVED,
    )

    expected = f"{patient.email} ↔ {doctor.email} [cardiology] - {STATUS_APPROVED}"
    assert str(link) == expected
