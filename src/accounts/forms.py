from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from accounts.models import Profile
from accounts.choices import UserRoles
from common.mixins import FormHelperMixin

UserModel = get_user_model()


class AppUserCreationForm(FormHelperMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ["email", "role", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [
            (UserRoles.PATIENT, "Patient"),
            (UserRoles.DOCTOR, "Doctor"),
        ]

    def save(self, commit=True):
        user = super().save(commit=commit)
        return user


class AppUserChangeForm(FormHelperMixin, UserChangeForm):
    class Meta:
        model = UserModel
        fields = ['email']


class LoginForm(FormHelperMixin, AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": "Email", "class": "form-control"})
    )


class ProfileBaseForm(FormHelperMixin, forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message="Enter a valid phone number (7 to 15 digits, optional + at the start)."
            )
        ],
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'date_of_birth', 'gender', 'phone']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class ProfileEditForm(ProfileBaseForm):
    pass



class PatientRegisterForm(AppUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].initial = UserRoles.PATIENT
        self.fields["role"].widget = forms.HiddenInput()


class DoctorRegisterForm(AppUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].initial = UserRoles.DOCTOR
        self.fields["role"].widget = forms.HiddenInput()
