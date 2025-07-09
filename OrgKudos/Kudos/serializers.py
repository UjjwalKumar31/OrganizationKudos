"""
Serializers for the Kudos application.

This module defines serializers used for user authentication, user representation,
and managing Kudo interactions, including sending and viewing kudos.

Serializers:
    - SignupSerializer: Handles user registration with secure password storage.
    - LoginSerializer: Authenticates users based on username and password.
    - KudoSerializer: Serializes Kudo objects for display purposes.
    - GiveKudoSerializer: Validates and processes the creation of new Kudos.
    - UserSerializer: Returns user profile data along with remaining weekly kudos.

These serializers enforce business rules such as:
    - Only 3 kudos can be sent per user per week.
    - Kudos can only be sent to users in the same organization.
    - Users cannot send kudos to themselves.
"""

from rest_framework import serializers
from .models import User, Kudo, Organization
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup/registration.

    Fields:
    - username: Required. User's login name.
    - password: Required. Write-only field for user password.
    - organization: Required. Organization the user belongs to (referenced by ID).

    This serializer handles user creation using Django's `create_user` method.
    """
    password = serializers.CharField(write_only=True)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = User
        fields = ['username', 'password', 'organization']

    def create(self, validated_data):
        """
        Create a new user using Django's secure password handling.
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
    - username: Required. User's login name.
    - password: Required. User's password.

    Validates user credentials and returns the authenticated user if valid.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Authenticate the user with provided username and password.
        """
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data


class KudoSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing Kudos.

    Fields:
    - id: Kudo ID
    - sender: Name of the user who sent the kudo (read-only)
    - receiver: Name of the user who received the kudo (read-only)
    - message: Kudo message content
    - created_at: Timestamp of when the kudo was sent
    """
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Kudo
        fields = ['id', 'sender', 'receiver', 'message', 'created_at']


class GiveKudoSerializer(serializers.ModelSerializer):
    """
    Serializer for sending (giving) a Kudo.

    Fields:
    - receiver: Required. The user who will receive the kudo.
    - message: Required. The appreciation message.

    Behavior:
    - Prevents sending kudos to self.
    - Ensures kudos can only be given within the same organization.
    - Enforces weekly kudos limit using `User.kudos_left()` method.
    """

    class Meta:
        model = Kudo
        fields = ['receiver', 'message']

    def __init__(self, *args, **kwargs):
        """
        Dynamically filter the 'receiver' queryset to exclude the sender (current user).
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['receiver'].queryset = User.objects.exclude(id=request.user.id)

    def validate(self, data):
        """
        Validate that:
        - The user has remaining kudos to give this week.
        - The receiver is in the same organization.
        """
        user = self.context['request'].user
        if user.kudos_left() <= 0:
            raise serializers.ValidationError("You have no kudos left this week.")
        if user.organization != data['receiver'].organization:
            raise serializers.ValidationError("Receiver must be in your organization.")
        return data

    def create(self, validated_data):
        """
        Attach the current user as the sender before saving the Kudo.
        """
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning user details, including:
    - id
    - username
    - organization name (not ID)
    - number of kudos left this week
    """
    kudos_left = serializers.SerializerMethodField()
    organization = serializers.StringRelatedField()  # Uses Organization.__str__()

    class Meta:
        model = User
        fields = ['id', 'username', 'organization', 'kudos_left']

    def get_kudos_left(self, obj):
        """
        Return the number of kudos the user has left to give this week.
        """
        return obj.kudos_left()
