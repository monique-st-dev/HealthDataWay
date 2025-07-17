from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from accounts.models import Profile, DoctorData
from accounts.choices import UserRoles
from accounts.validators import validate_diploma_issue_date
from common.mixins import FormHelperMixin

UserModel = get_user_model()


class AppUserCreationForm(FormHelperMixin, UserCreationForm):
    diploma_number = forms.CharField(
        max_length=50,
        required=False,
        label="Diploma Number",
        help_text="Required only for doctors.",
    )
    diploma_issue_date = forms.DateField(
        required=False,
        label="Diploma Issue Date",
        help_text="Required only for doctors.",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control',
                                      'placeholder': 'YYYY-MM-DD',}),
        validators=[validate_diploma_issue_date],
    )

    class Meta:
        model = UserModel
        fields = ["email", "role", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [
            (UserRoles.PATIENT, "Patient"),
            (UserRoles.DOCTOR, "Doctor"),
        ]

        role = self.initial.get("role") or getattr(self.instance, "role", None)

        if role != UserRoles.DOCTOR:
            self.fields.pop("diploma_number", None)
            self.fields.pop("diploma_issue_date", None)

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")

        if role == UserRoles.DOCTOR:
            if not cleaned_data.get("diploma_number"):
                self.add_error("diploma_number", "Diploma number is required for doctors.")
            if not cleaned_data.get("diploma_issue_date"):
                self.add_error("diploma_issue_date", "Diploma issue date is required for doctors.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        if user.role == UserRoles.DOCTOR:
            DoctorData.objects.create(
                user=user,
                diploma_number=self.cleaned_data["diploma_number"],
                diploma_issue_date=self.cleaned_data["diploma_issue_date"],
            )
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
        fields = ['full_name', 'date_of_birth', 'gender', 'phone', 'image']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class ProfileEditForm(ProfileBaseForm):
    pass


class DoctorDataForm(FormHelperMixin, forms.ModelForm):
    class Meta:
        model = DoctorData
        fields = ['diploma_number', 'diploma_issue_date', 'specialization']
        widgets = {
            'diploma_issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


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
