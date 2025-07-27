from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from accounts.views import (
    CustomLoginView,
    CustomLogoutView,
    ProfileDetailView,
    ProfileEditView,
    RegisterChoiceView,
    RegisterDoctorView,
    RegisterPatientView,
    ProfileDeleteView,
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('register/', RegisterChoiceView.as_view(), name='register_choice'),
    path('register/doctor/', RegisterDoctorView.as_view(), name='register_doctor'),
    path('register/patient/', RegisterPatientView.as_view(), name='register_patient'),

    path('profile/', ProfileDetailView.as_view(), name='profile-details'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit-profile'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='delete-profile'),


    path(
        'password/change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            success_url=reverse_lazy('password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done',
    ),
]
