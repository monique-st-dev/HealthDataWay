from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser, Profile, DoctorPatientLink


class Command(BaseCommand):
    help = "Assigns predefined permissions to Staff group"

    def handle(self, *args, **options):
        try:
            staff_group, _ = Group.objects.get_or_create(name="Staff")

            models_and_perms = {
                CustomUser: ['view'],
                Profile: ['view', 'change'],
                DoctorPatientLink: ['view'],
            }

            for model, actions in models_and_perms.items():
                ct = ContentType.objects.get_for_model(model)
                for action in actions:
                    codename = f"{action}_{model._meta.model_name}"
                    perm = Permission.objects.get(codename=codename, content_type=ct)
                    staff_group.permissions.add(perm)
                    self.stdout.write(self.style.SUCCESS(f"Added: {codename}"))

            self.stdout.write(self.style.SUCCESS("Permissions assigned to Staff group successfully."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error assigning permissions: {e}"))
