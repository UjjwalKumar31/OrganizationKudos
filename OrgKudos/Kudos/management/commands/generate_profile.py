# python manage.py generate_profile
"""
Management command to generate demo data for the Kudos application.

This command populates the database with:
- A predefined set of organizations.
- Random users assigned to those organizations.
- (Optionally) random Kudos exchanged between users.

Usage:
    python manage.py generate_profile

Intended for use in development, testing, or demo environments.
"""
from django.core.management.base import BaseCommand
from Kudos.models import User, Organization, Kudo
from faker import Faker
import random

class Command(BaseCommand):
    """
    Django custom management command to generate demo data for Kudos.

    Functionality:
        - Deletes existing data from Organization, User, and Kudo models.
        - Creates a set of predefined organizations.
        - Generates fake users using the Faker library and assigns them to organizations.
        - (Optionally) generates random kudos between users.

    The command prints the created usernames and passwords for easy testing.
    """

    help = 'Generate demo data for testing or demo purposes.'

    def handle(self, *args, **kwargs):
        """
        Executes the data generation process.

        Steps:
            1. Deletes all existing Kudo, User, and Organization records.
            2. Creates predefined organizations (Mitratech, Deloitte, Capgemini).
            3. Generates 7 users with fake usernames and a common demo password.
            4. Optionally, generates 10 random Kudos between users (currently commented out).

        Outputs:
            Prints created users (username/password) to console.
        """
        fake = Faker()

        # Step 1: Clear all existing data
        Kudo.objects.all().delete()
        User.objects.all().delete()
        Organization.objects.all().delete()

        # Step 2: Create some predefined and random organizations
        org_list = ['Mitratech', 'Deloitte', 'Capgemini']
        orgs = [Organization.objects.create(name=name) for name in org_list]

        print("🔐 Generated Users (username / password):")

        users = []

        # Step 3: Create fake users and assign them to random organizations
        for _ in range(11):
            username = fake.user_name()
            password = "test1234"  # Use a common password for demo users
            org = random.choice(orgs)
            user = User.objects.create_user(username=username, password=password, organization=org)
            users.append(user)
            print(f" - {username} / {password}")

        # Step 4 (Optional): Create some random Kudos between users
        # Uncomment the block below to auto-generate Kudos

        # for _ in range(10):
        #     sender, receiver = random.sample(users, 2)
        #     Kudo.objects.create(
        #         sender=sender,
        #         receiver=receiver,
        #         message=fake.sentence()
        #     )

        self.stdout.write(self.style.SUCCESS("✅ Demo data generated successfully."))
