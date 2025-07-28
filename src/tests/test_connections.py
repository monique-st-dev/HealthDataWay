import pytest
from django.contrib.auth import get_user_model
from connections.forms import DoctorAddPatientForm
from connections.models import DoctorPatientLink
from connections.choices import STATUS_PENDING, DIRECTION_CHOICES

User = get_user_model()


@pytest.mark.django_db
def test_add_patient_form_success():
    doctor = User.objects.create_user(email='doc@example.com', password='pass123', role='doctor')
    patient = User.objects.create_user(email='pat@example.com', password='pass123', role='patient')

    form = DoctorAddPatientForm(
        data={'patient_email': 'pat@example.com', 'direction': DIRECTION_CHOICES[0][0]},
        doctor=doctor
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_add_patient_form_invalid_email():
    doctor = User.objects.create_user(email='doc@example.com', password='pass123', role='doctor')

    form = DoctorAddPatientForm(
        data={'patient_email': 'notfound@example.com', 'direction': DIRECTION_CHOICES[0][0]},
        doctor=doctor
    )
    assert not form.is_valid()
    assert 'patient_email' in form.errors


@pytest.mark.django_db
def test_add_patient_form_existing_link():
    doctor = User.objects.create_user(email='doc@example.com', password='pass123', role='doctor')
    patient = User.objects.create_user(email='pat@example.com', password='pass123', role='patient')

    DoctorPatientLink.objects.create(
        doctor=doctor, patient=patient,
        direction=DIRECTION_CHOICES[0][0],
        status=STATUS_PENDING
    )

    form = DoctorAddPatientForm(
        data={'patient_email': 'pat@example.com', 'direction': DIRECTION_CHOICES[0][0]},
        doctor=doctor
    )
    assert not form.is_valid()
    assert '__all__' in form.errors


@pytest.mark.django_db
def test_doctor_patient_link_unique_constraint():
    doctor = User.objects.create_user(email='doc@example.com', password='pass123', role='doctor')
    patient = User.objects.create_user(email='pat@example.com', password='pass123', role='patient')

    DoctorPatientLink.objects.create(
        doctor=doctor, patient=patient,
        direction=DIRECTION_CHOICES[0][0],
        status=STATUS_PENDING
    )

    with pytest.raises(Exception):
        DoctorPatientLink.objects.create(
            doctor=doctor, patient=patient,
            direction=DIRECTION_CHOICES[0][0],
            status=STATUS_PENDING
        )


@pytest.mark.django_db
def test_doctor_patient_link_str():
    doctor = User.objects.create_user(email='doc@example.com', password='pass123', role='doctor')
    patient = User.objects.create_user(email='pat@example.com', password='pass123', role='patient')

    link = DoctorPatientLink.objects.create(
        doctor=doctor, patient=patient,
        direction=DIRECTION_CHOICES[0][0],
        status=STATUS_PENDING
    )

    expected = f"{patient.email} ↔ {doctor.email} [{link.direction}] - {link.status}"
    assert str(link) == expected
