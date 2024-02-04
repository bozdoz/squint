import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        username = os.environ.get('SU_USER')
        email = os.environ.get('SU_EMAIL')
        password = os.environ.get('SU_PASS')
        if email and not User.objects.filter(email=email).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print('superuser created!')
        else:
            print('not making superuser!')
