import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_patient(client):
    url = reverse('register_patient')
    data = {
        'email': 'patient@example.com',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(email='patient@example.com').exists()


@pytest.mark.django_db
def test_register_doctor(client):
    url = reverse('register_doctor')
    data = {
        'email': 'doctor@example.com',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
        'license_number': '123456',
        'license_date': '2020-01-01',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(email='doctor@example.com').exists()


@pytest.mark.django_db
def test_edit_profile_view_access(client, django_user_model):
    user = django_user_model.objects.create_user(email='test@example.com', password='StrongPass123!')
    client.login(email='test@example.com', password='StrongPass123!')
    url = reverse('edit_profile')
    response = client.get(url)
    assert response.status_code == 200
