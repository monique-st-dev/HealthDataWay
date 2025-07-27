from django.urls import path
from connections import views
from connections.views.doctor import DoctorPatientReportView

urlpatterns = [
    # Doc
    path('doctor/add/', views.DoctorCreateLinkView.as_view(), name='doctor-add-patient'),
    path('doctor/patients/', views.DoctorPatientsListView.as_view(), name='doctor-patients-list'),
    path('doctor/patients/<int:pk>/cancel/', views.DoctorCancelLinkView.as_view(), name='doctor-cancel-link'),
    path('doctor/patients/<int:pk>/details/', views.DoctorPatientDetailView.as_view(), name='doctor-patient-detail'),
    path('doctor/patients/<int:pk>/report/', DoctorPatientReportView.as_view(), name='doctor-patient-report'),
    # Patient
    path('patient/requests/', views.PatientConnectionRequestsView.as_view(), name='patient-requests'),
    path('patient/requests/<int:pk>/respond/', views.PatientRespondView.as_view(), name='patient-respond'),
    path('patient/connections/', views.PatientConnectionsView.as_view(), name='patient-connections'),
    path('patient/connections/<int:pk>/disconnect/', views.PatientDisconnectView.as_view(), name='disconnect-doctor'),
]
