import pytest
from django.urls import reverse
from django.utils import timezone
from notifications.models import Notification
from accounts.models import CustomUser


@pytest.mark.django_db
def test_notification_list_view(client):
    user = CustomUser.objects.create_user(email="patient@example.com", password="pass1234", role="patient")
    Notification.objects.create(
        recipient=user,
        message="Test notification",
        notification_type="reminder",
    )

    client.login(email="patient@example.com", password="pass1234")
    response = client.get(reverse("notification_list"))

    assert response.status_code == 200
    assert "notifications" in response.context
    assert len(response.context["notifications"]) == 1
    assert response.context["notifications"][0].message == "Test notification"


@pytest.mark.django_db
def test_mark_notifications_as_read_view(client):
    user = CustomUser.objects.create_user(email="doctor@example.com", password="pass1234", role="doctor")
    notification = Notification.objects.create(
        recipient=user,
        message="New appointment",
        notification_type="info",
        is_read=False,
    )

    client.login(email="doctor@example.com", password="pass1234")
    url = reverse("mark_notifications_as_read")
    response = client.get(url)

    assert response.status_code == 200
    notification.refresh_from_db()
    assert notification.is_read is True


@pytest.mark.django_db
def test_mark_single_notification_as_read(client):
    user = CustomUser.objects.create_user(email="patient2@example.com", password="pass1234", role="patient")
    notification = Notification.objects.create(
        recipient=user,
        message="Chart updated",
        notification_type="reminder",
        is_read=False,
    )

    client.login(email="patient2@example.com", password="pass1234")
    url = reverse("mark_notification_as_read", kwargs={"pk": notification.pk})
    response = client.post(url)

    assert response.status_code == 200
    notification.refresh_from_db()
    assert notification.is_read is True
