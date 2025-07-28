from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from accounts.models import Profile
from accounts.choices import UserRoles

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_related_user_data(sender, instance, created, **kwargs):
    if not created or instance.is_superuser:
        return

    if not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)

    role_to_group = {
        UserRoles.DOCTOR: "Doctor",
        UserRoles.PATIENT: "Patient",
    }

    if instance.is_staff and not instance.is_superuser:
        group, _ = Group.objects.get_or_create(name="Staff")
        instance.groups.add(group)
    elif instance.role in role_to_group:
        group_name = role_to_group[instance.role]
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


