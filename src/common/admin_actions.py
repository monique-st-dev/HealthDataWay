from django.contrib import messages
from django.contrib.auth.models import Group

ROLE_GROUPS = {"Staff", "Doctor", "Patient"}

def _assign_group(request, queryset, target_group_name):
    target_group, _ = Group.objects.get_or_create(name=target_group_name)

    added_count = 0
    already_in_group = 0
    switched_group = 0

    for user in queryset:
        if user.is_superuser:
            continue

        current_groups = set(g.name for g in user.groups.all())

        if target_group_name in current_groups and current_groups & ROLE_GROUPS == {target_group_name}:
            already_in_group += 1
            continue


        for group_name in ROLE_GROUPS:
            if group_name != target_group_name:
                group = Group.objects.filter(name=group_name).first()
                if group and group in user.groups.all():
                    user.groups.remove(group)
                    switched_group += 1


        user.groups.add(target_group)
        added_count += 1

    if added_count:
        messages.success(request, f"{added_count} user(s) added to '{target_group_name}' group.")
    if switched_group:
        messages.warning(request, f"{switched_group} user(s) were moved from other groups.")
    if already_in_group:
        messages.info(request, f" {already_in_group} user(s) were already in '{target_group_name}' group only.")


def assign_to_staff_group(modeladmin, request, queryset):
    _assign_group(request, queryset, "Staff")
assign_to_staff_group.short_description = "Add to Staff group"

def assign_to_doctor_group(modeladmin, request, queryset):
    _assign_group(request, queryset, "Doctor")
assign_to_doctor_group.short_description = "Add to Doctor group"

def assign_to_patient_group(modeladmin, request, queryset):
    _assign_group(request, queryset, "Patient")
assign_to_patient_group.short_description = "Add to Patient group"


def deactivate_users(modeladmin, request, queryset):
    updated = queryset.exclude(is_superuser=True).update(is_active=False)
    messages.warning(request, f"{updated} user(s) deactivated (superusers skipped).")
deactivate_users.short_description = "Deactivate selected users"

def activate_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    messages.success(request, f"{updated} user(s) activated.")
activate_users.short_description = "Activate selected users"