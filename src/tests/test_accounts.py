import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_patient(client):
    url = reverse('register_patient')
    data = {
        'email': 'patient@example.com',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
        'role': 'patient',
    }
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_register_doctor(client):
    url = reverse('register_doctor')
    data = {
        'email': 'doctor@example.com',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
        'license_number': '123456',
        'license_date': '2020-01-01',
        'role': 'doctor',
    }
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_profile_view_access(client, django_user_model):
    user = django_user_model.objects.create_user(email='test@example.com', password='pass1234')
    client.login(email='test@example.com', password='pass1234')
    url = reverse('edit-profile')
    response = client.get(url)
    assert response.status_code == 200
