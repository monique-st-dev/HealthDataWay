from django.urls import path
from .views import NotificationListView, mark_notifications_as_read, MarkNotificationAsReadView, DeleteNotificationView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('mark-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path('mark-as-read/<int:pk>/', MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),
    path('delete/<int:pk>/', DeleteNotificationView.as_view(), name='notification_delete'),
]
