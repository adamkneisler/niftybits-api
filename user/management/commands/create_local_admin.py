from django.core.management.base import BaseCommand, CommandError
from user.models import NiftyUser
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates an admin user into local database'

    def handle(self, *args, **options):
            username = 'admin'
            password = "niftyadmin123"

            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.first_name = username
            user.save()

            nifty_user, created = NiftyUser.objects.get_or_create(
                user = user,
            )
            nifty_user.save()
