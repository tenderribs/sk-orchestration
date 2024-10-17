from django.core.management.base import BaseCommand

from .connectors.innet_pull import innet_main


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        innet_main()
        self.stdout.write(self.style.SUCCESS("Imported INNET data"))
