from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Seeds the database with an initial admin user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin_email = 'admin@gmail.com'
        admin_password = 'AdminPassword@123'

        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password=admin_password,
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {admin_email}'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user already exists: {admin_email}'))
