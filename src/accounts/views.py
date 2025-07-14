from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from accounts.choices import UserRoles
from accounts.forms import (
    LoginForm,
    ProfileEditForm,
    DoctorRegisterForm,
    PatientRegisterForm,
)
from accounts.models import CustomUser, Profile

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")

class RegisterChoiceView(TemplateView):
    template_name = "accounts/register_choice.html"


class RegisterPatientView(CreateView):
    model = CustomUser
    form_class = PatientRegisterForm
    template_name = "accounts/register_patient.html"
    success_url = reverse_lazy("dashboard")

    def get_initial(self):
        return {'role': UserRoles.PATIENT}

    def form_valid(self, form):
        form.instance.role = UserRoles.PATIENT
        response = super().form_valid(form)
        login(self.request, self.object)
        return response




class RegisterDoctorView(CreateView):
    model = CustomUser
    form_class = DoctorRegisterForm
    template_name = "accounts/register_doctor.html"
    success_url = reverse_lazy("dashboard")

    def get_initial(self):
        return {'role': UserRoles.DOCTOR}

    def form_valid(self, form):
        form.instance.role = UserRoles.DOCTOR
        response = super().form_valid(form)
        login(self.request, self.object)
        return response



class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        return self.request.user.profile.pk == self.kwargs.get("pk")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


@login_required
def app_user_delete_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk, user=request.user)
    user = profile.user
    user.delete()
    return redirect("home")
