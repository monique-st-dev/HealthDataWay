from django.urls import path

from accounts.views import (
    CustomLoginView,
    CustomLogoutView,
    ProfileDetailView,
    ProfileEditView,
    app_user_delete_view, RegisterChoiceView, RegisterDoctorView, RegisterPatientView,
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('register/', RegisterChoiceView.as_view(), name='register_choice'),
    path('register/doctor/', RegisterDoctorView.as_view(), name='register_doctor'),
    path('register/patient/', RegisterPatientView.as_view(), name='register_patient'),

    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-details'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='edit-profile'),
    path('profile/<int:pk>/delete/', app_user_delete_view, name='delete-profile'),

]