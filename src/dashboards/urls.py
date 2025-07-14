from django.urls import path
from dashboards.views import (
    DashboardRedirectView,
    DoctorDashboardView,
    PatientDashboardView
)

urlpatterns = [
    path('', DashboardRedirectView.as_view(), name='dashboard'),
    path('doctor/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('patient/', PatientDashboardView.as_view(), name='patient_dashboard'),
]
