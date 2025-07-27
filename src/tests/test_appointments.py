import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from accounts.models import CustomUser
from appointments.models import Appointment
from connections.models import DoctorPatientLink
from connections.choices import STATUS_APPROVED


@pytest.mark.django_db
def test_patient_creates_appointment(client):
    doctor = CustomUser.objects.create_user(email='doc@app.com', password='pass', role='doctor')
    patient = CustomUser.objects.create_user(email='pat@app.com', password='pass', role='patient')

    DoctorPatientLink.objects.create(
        doctor=doctor,
        patient=patient,
        direction='endocrinology',
        status=STATUS_APPROVED,
    )

    client.force_login(patient)

    appointment_time = (timezone.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)

    response = client.post(reverse('appointment_create'), {
        'doctor': doctor.pk,
        'appointment_datetime': appointment_time.strftime('%Y-%m-%dT%H:%M'),
        'reason': 'Test appointment',
    })

    assert response.status_code == 302
    assert Appointment.objects.filter(patient=patient, doctor=doctor).exists()


@pytest.mark.django_db
def test_doctor_approves_appointment(client):
    doctor = CustomUser.objects.create_user(email='doc2@app.com', password='pass', role='doctor')
    patient = CustomUser.objects.create_user(email='pat2@app.com', password='pass', role='patient')

    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        appointment_datetime=timezone.now() + timedelta(days=2),
        reason='Test approve',
        is_confirmed=False,
    )

    client.force_login(doctor)
    response = client.post(reverse('appointment_approve', args=[appointment.pk]))

    appointment.refresh_from_db()
    assert response.status_code == 302
    assert appointment.is_confirmed is True


@pytest.mark.django_db
def test_doctor_rejects_appointment(client):
    doctor = CustomUser.objects.create_user(email='doc3@app.com', password='pass', role='doctor')
    patient = CustomUser.objects.create_user(email='pat3@app.com', password='pass', role='patient')

    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        appointment_datetime=timezone.now() + timedelta(days=3),
        reason='Test reject',
        is_confirmed=False,
    )

    client.force_login(doctor)
    response = client.post(reverse('appointment_reject', args=[appointment.pk]))

    assert response.status_code == 302
    assert not Appointment.objects.filter(pk=appointment.pk).exists()
