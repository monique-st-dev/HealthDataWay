from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from accounts.choices import UserRoles
from accounts.forms import (
    LoginForm,
    ProfileEditForm,
    DoctorRegisterForm,
    PatientRegisterForm,
)
from accounts.models import CustomUser, Profile

UserModel = get_user_model()

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


from django.shortcuts import render

class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out.")
        return render(request, self.template_name)


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



class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was a problem updating your profile.")
        return super().form_invalid(form)



class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "accounts/profile-delete-page.html"


    def get_object(self, queryset=None):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)

        user.delete()

        return render(request, "accounts/logout.html")