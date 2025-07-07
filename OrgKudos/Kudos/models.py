from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Organization(models.Model):
    """
    Represents an organization or company.
    Users belong to organizations.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds a ForeignKey to Organization and methods for kudos limits.
    """
    organization = models.ForeignKey(
                    Organization,
                    on_delete=models.CASCADE,
                    null=True,  # ✅ allow NULL values
                    blank=True  # ✅ allow empty values in forms
                )

    def kudos_given_this_week(self):
        """
        Returns the number of kudos the user has given since the start of the current week.
        """
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.sent_kudos.filter(created_at__gte=start_of_week).count()

    def kudos_left(self):
        """
        Returns how many kudos this user has left to give this week.
        Max allowed kudos per week is 3.
        """
        return max(0, 3 - self.kudos_given_this_week())

class Kudo(models.Model):
    """
    Model representing a 'kudo' — a message of appreciation sent from one user to another.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_kudos')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_kudos')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Custom validation: ensure sender and receiver belong to the same organization.
        """
        if self.sender.organization != self.receiver.organization:
            raise ValidationError("Cannot give kudos outside your organization.")
