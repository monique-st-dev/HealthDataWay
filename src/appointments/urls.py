from django.urls import path
from appointments.views.patient import (
    AppointmentCreateView,
    AppointmentListView,
)
from appointments.views.doctor import (
    DoctorAppointmentListView,
)
from appointments.views.actions import (
    ApproveAppointmentView,
    RejectAppointmentView,
    CancelConfirmedAppointmentView,
)

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('my/', AppointmentListView.as_view(), name='appointment_list'),
    path('doctor/', DoctorAppointmentListView.as_view(), name='doctor_appointment_list'),
    path('<int:pk>/approve/', ApproveAppointmentView.as_view(), name='appointment_approve'),
    path('<int:pk>/reject/', RejectAppointmentView.as_view(), name='appointment_reject'),
    path('<int:pk>/cancel/', CancelConfirmedAppointmentView.as_view(), name='appointment_cancel'),
]
