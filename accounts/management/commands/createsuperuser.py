from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from django.db.utils import IntegrityError


class Command(BaseCommand):
    """
    Create an admin user that can only log in via Google OAuth (no local password).
    It asks for an email, sets is_staff/is_superuser, and creates a UserSocialAuth entry.
    """

    help = "Create an admin user (superuser) with Google OAuth login only."

    def add_arguments(self, parser):
        parser.add_argument('--email', help='Email address for the new admin user')

    def handle(self, *args, **options):
        email = options['email']
        if not email:
            email = input('Enter email address: ').strip()

        if not email:
            raise CommandError("Email cannot be empty.")

        user_model = get_user_model()

        try:
            user, created = user_model.objects.get_or_create(email=email, defaults={
                "username": email,
            })

            user.is_staff = True
            user.is_superuser = True
            user.is_active = True

            user.set_unusable_password()
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Admin user created: {email}"))

            UserSocialAuth.objects.get_or_create(
                user=user, provider='google-oauth2', defaults={"uid": email}
            )

            UserSocialAuth.objects.get_or_create(
                user=user, provider='microsoft-graph', defaults={"uid": email}
            )

            UserSocialAuth.objects.get_or_create(
                user=user, provider='facebook', defaults={"uid": email}
            )

            self.stdout.write(self.style.SUCCESS(
                f"Linked {email} to Google OAuth2, Microsoft Graph, and Facebook OAuth2"
            ))

        except IntegrityError:
            raise CommandError("Error creating user")

