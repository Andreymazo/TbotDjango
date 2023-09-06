from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            username='andreymazo@mail.ru',
            is_superuser=True,
            is_staff=True
        )
        user.set_password('qwert123asd')
        user.is_superuser = True

        user.save()
        # from django.db import connection
        # db_name = connection.settings_dict['NAME']
        # print(db_name)

        # python-dotenv example
        # import os
        # from dotenv import load_dotenv
        # load_dotenv()

        # print(os.getenv("DB_NAME"))