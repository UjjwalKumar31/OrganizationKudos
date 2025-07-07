# python manage.py generate_profile

from django.core.management.base import BaseCommand
from Kudos.models import User, Organization, Kudo
from faker import Faker
import random

class Command(BaseCommand):
    """
    Django custom management command to generate demo data.
    It creates:
    - Sample organizations
    - Random users with fake usernames
    - (Optionally) random kudos between users
    """

    help = 'Generate demo data for testing or demo purposes.'

    def handle(self, *args, **kwargs):
        """
        Main logic for generating demo data.
        Deletes existing records and repopulates the database
        with fake users and organizations.
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
        for _ in range(7):
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
