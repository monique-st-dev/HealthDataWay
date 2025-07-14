from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

UserModel = get_user_model()

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    groups_to_create = ["Admin", "Staff", "Doctor", "Patient"]

    for group_name in groups_to_create:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Group created: {group_name}")
        else:
            print(f"Group already exists: {group_name}")


    staff_group = Group.objects.get(name="Staff")
    permissions = Permission.objects.filter(codename__in=[
        "view_customuser", "change_customuser",
        "view_profile", "change_profile",
        "view_healthdata",
        "add_customuser",
    ])
    staff_group.permissions.set(permissions)

@receiver(post_save, sender=UserModel)
def add_staff_to_staff_group(sender, instance, created, **kwargs):
    if created and instance.is_staff and not instance.is_superuser:
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        instance.groups.add(staff_group)