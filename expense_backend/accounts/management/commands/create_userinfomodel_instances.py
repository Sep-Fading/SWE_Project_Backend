from django.core.management.base import BaseCommand
from accounts.models import AccountModel, UserInfoModel

class Command(BaseCommand):
    help = 'Creates UserInfoModel instances for each AccountModel'

    def handle(self, *args, **options):
        for account in AccountModel.objects.all():
            UserInfoModel.objects.get_or_create(user_id=account)
        self.stdout.write(self.style.SUCCESS('Successfully created UserInfoModel instances'))

