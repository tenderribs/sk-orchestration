import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings


from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Set up groups and permissions according to spec"

    def setup_groups(self):
        # User for the partner org connector functions. Minimal subset of operations
        Group.objects.create(name="connectors").permissions.set(
            [
                Permission.objects.get(codename="add_measurement"),
                Permission.objects.get(codename="view_installation"),
                Permission.objects.get(codename="view_logger"),
            ]
        )

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

    def setup_conn_user(self):
        # Create connection service user that interacts with
        conn_user, created = User.objects.get_or_create(username=os.environ["CONN_USER"])

        if created:
            conn_user.set_password(os.environ["CONN_PASSWORD"])
            conn_user.save()  # ensures password is hashed

        conn_group = Group.objects.get(name="connectors")  # add to group for correct perms
        conn_user.groups.add(conn_group)

        # Generate API token for the user
        Token.objects.create(key=os.environ["CONN_TOKEN"], user=conn_user)

        # Create example user for use with Session auth
        if settings.DEBUG:
            ugz_user = User.objects.create(username="ugz")
            ugz_user.set_password("superlit")
            ugz_user.save()  # ensures password is hashed

            frontend_group = Group.objects.get(name="frontend")
            ugz_user.groups.add(frontend_group)

    def handle(self, *args, **kwargs):
        self.setup_groups()
        self.stdout.write(self.style.SUCCESS("Created Groups"))

        self.setup_conn_user()
        self.stdout.write(self.style.SUCCESS("Generated Connector User and Auth Token"))
