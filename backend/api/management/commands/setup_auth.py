from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings


class Command(BaseCommand):
    help = "Set up groups and permissions according to spec"

    def setup_groups(self):
        # Basic CRUD user for frontend ajax applications using session auth.
        Group.objects.create(name="frontend").permissions.set(
            [
                Permission.objects.get(codename="add_site"),
                Permission.objects.get(codename="change_site"),
                Permission.objects.get(codename="delete_site"),
                Permission.objects.get(codename="view_site"),
                Permission.objects.get(codename="add_devicemodel"),
                Permission.objects.get(codename="change_devicemodel"),
                Permission.objects.get(codename="delete_devicemodel"),
                Permission.objects.get(codename="view_devicemodel"),
                Permission.objects.get(codename="add_logger"),
                Permission.objects.get(codename="change_logger"),
                Permission.objects.get(codename="delete_logger"),
                Permission.objects.get(codename="view_logger"),
                Permission.objects.get(codename="add_installation"),
                Permission.objects.get(codename="change_installation"),
                Permission.objects.get(codename="delete_installation"),
                Permission.objects.get(codename="view_installation"),
                Permission.objects.get(codename="add_measurement"),
                Permission.objects.get(codename="change_measurement"),
                Permission.objects.get(codename="delete_measurement"),
                Permission.objects.get(codename="view_measurement"),
            ]
        )

    def setup_dev_user(self):
        """Create example user for use with Session auth"""
        ugz_user = User.objects.create(username="ugz", is_staff=True)
        ugz_user.set_password("superlit")
        ugz_user.save()  # ensures password is hashed

        frontend_group = Group.objects.get(name="frontend")
        ugz_user.groups.add(frontend_group)

    def handle(self, *args, **kwargs):
        self.setup_groups()
        self.stdout.write(self.style.SUCCESS("Created Groups"))

        if settings.DEBUG:
            self.setup_conn_user()
            self.stdout.write(
                self.style.SUCCESS("Generated dev User (SHOULDN'T SEE THIS MSG IN PROD)")
            )
