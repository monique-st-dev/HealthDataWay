from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from accounts.forms import AppUserCreationForm, AppUserChangeForm
from accounts.models import Profile, DoctorData, DoctorPatientLink

from common.admin_actions import (
    assign_to_staff_group,
    deactivate_users,
    activate_users,
    assign_to_doctor_group,
    assign_to_patient_group,
)

UserModel = get_user_model()

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel
    add_form = AppUserCreationForm
    form = AppUserChangeForm

    list_display = ("email", "role", "get_groups", "is_staff", "is_superuser", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    list_editable = ("is_active",)
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Role", {"fields": ("role",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_active", "is_staff", "is_superuser", "groups"),
        }),
    )

    readonly_fields = ("last_login", "date_joined")
    actions = [
        assign_to_staff_group,
        assign_to_doctor_group,
        assign_to_patient_group,
        deactivate_users,
        activate_users,
    ]

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = "Groups"



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile

    list_display = ("user", "full_name", "phone", "gender")
    list_filter = ("gender",)
    search_fields = ("user__email", "full_name", "phone")
    ordering = ("user__email",)

    def has_add_permission(self, request):
        return False

@admin.register(DoctorData)
class DoctorDataAdmin(admin.ModelAdmin):
    model = DoctorData

    list_display = ("user", "diploma_number", "diploma_issue_date", "specialization")
    search_fields = ("user__email", "diploma_number", "specialization")
    ordering = ("user__email",)

    def has_add_permission(self, request):
        return False


@admin.register(DoctorPatientLink)
class DoctorPatientLinkAdmin(admin.ModelAdmin):
    model = DoctorPatientLink

    list_display = ("doctor", "patient", "created_at")
    list_filter = ("doctor",)
    search_fields = ("doctor__email", "patient__email")
    ordering = ("-created_at",)

