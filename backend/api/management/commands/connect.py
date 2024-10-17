from django.core.management.base import BaseCommand

from .connectors.innet_pull import main as innet_main
from .connectors.meteoblue_pull import main as meteoblue_main


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        innet_main()
        self.stdout.write(self.style.SUCCESS("Imported INNET data"))

        meteoblue_main()
        self.stdout.write(self.style.SUCCESS("Imported METEOBLUE data"))
