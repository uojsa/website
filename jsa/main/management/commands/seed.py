from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Event, EventSession
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the local database with initial test data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Just create superuser for now
        self.stdout.write("Creating superuser...")
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.SUCCESS("  Created superuser 'admin'"))
        else:
            self.stdout.write(self.style.WARNING("  Already Exists: superuser 'admin'"))

        self.stdout.write(self.style.SUCCESS("Database successfully seeded!"))
