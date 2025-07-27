from django.db import models
from django.conf import settings
from .notification_constants import NOTIFICATION_TYPES


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        limit_choices_to={'role__in': ['doctor', 'patient']},
        verbose_name="Recipient",
        help_text="User (doctor or patient) who will receive the notification.",
    )
    message = models.CharField(
        max_length=255,
        verbose_name="Message",
        help_text="The content of the notification.",
    )
    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        default='reminder',
        verbose_name="Notification Type",
        help_text="Type/category of the notification (e.g., reminder, info, etc).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date and time when the notification was created.",
        db_index=True,
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Is Read",
        help_text="Indicates whether the notification has been read.",
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
        ]

    def __str__(self):
        return f"Notification for {getattr(self.recipient, 'email', 'Unknown')}: {self.message}"

    def __repr__(self):
        return f"<Notification to={getattr(self.recipient, 'email', 'Unknown')} type={self.notification_type}>"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=["is_read"])
