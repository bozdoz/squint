from django.core.management.base import BaseCommand
from transactions.models import UserInstitution


class Command(BaseCommand):

    def handle(self, *args, **options):
        ui = UserInstitution.objects.first()
        print(ui)
