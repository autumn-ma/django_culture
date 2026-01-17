from django.core.management import BaseCommand

from core.models.user import User


class Command(BaseCommand):
    help = "Setup necessary data and configuration for the project."

    def handle(self, *args, **options):
        self.check_admin_user()

    def check_admin_user(self):
        self.stdout.write("Checking admin user.")
        admin_exists = User.objects.filter(is_superuser=True).exists()
        if admin_exists:
            self.stdout.write(
                "Admin user already exists. Skipping admin user creation."
            )
        else:
            self.stdout.write(
                "Admin user does not exist. Trying to create one from environment variables."
            )
            User.objects.create_superuser(
                username="admin",
                email="admin@admin.com",
                password="root",
            )
