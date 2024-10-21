from django.core.management.base import BaseCommand
from countries.utils import send_daily_notifications

class Command(BaseCommand):
    def handle(self, *args, **options):
        send_daily_notifications()
        self.stdout.write(self.style.SUCCESS('Successfully sent daily notifications.'))
