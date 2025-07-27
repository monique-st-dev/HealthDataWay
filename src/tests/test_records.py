import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import time

from accounts.models import CustomUser
from records.models import CardiologyRecord, EndocrinologyRecord


@pytest.mark.django_db
def test_create_endocrinology_record(client):
    user = CustomUser.objects.create_user(email="patient1@example.com", password="testpass", role="patient")
    client.force_login(user)
    url = reverse("add_endocrinology_record")
    data = {
        "blood_sugar": "6.2",
        "date": timezone.now().date(),
        "time": time(9, 30),
        "notes": "After breakfast",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert EndocrinologyRecord.objects.count() == 1


@pytest.mark.django_db
def test_create_cardiology_record(client):
    user = CustomUser.objects.create_user(email="patient2@example.com", password="testpass", role="patient")
    client.force_login(user)
    url = reverse("add_cardiology_record")
    data = {
        "systolic": 120,
        "diastolic": 80,
        "pulse": 75,
        "date": timezone.now().date(),
        "time": time(8, 0),
        "notes": "Morning check",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert CardiologyRecord.objects.count() == 1


@pytest.mark.django_db
def test_delete_cardiology_record(client):
    user = CustomUser.objects.create_user(email="patient3@example.com", password="testpass", role="patient")
    record = CardiologyRecord.objects.create(
        patient=user,
        systolic=130,
        diastolic=85,
        pulse=72,
        date=timezone.now().date(),
        time=time(7, 30),
    )
    client.force_login(user)
    url = reverse("delete_cardiology_record", kwargs={"pk": record.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert CardiologyRecord.objects.count() == 0
