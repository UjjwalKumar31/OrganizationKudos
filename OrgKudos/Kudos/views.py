"""
Views for the Kudos application.

This module defines class-based views for user authentication (signup, login, logout),
user-related information retrieval, and handling of Kudo objects (sending and listing).
It uses Django Rest Framework and Django’s generic views to handle HTTP requests.

Classes:
    HomePageView: Renders the homepage.
    SignupView: Handles user registration.
    LoginView: Handles user login.
    LogoutView: Logs out the authenticated user.
    MeView: Retrieves the authenticated user's profile.
    KudosReceivedView: Lists kudos received by the user.
    KudosGivenView: Lists kudos given by the user.
    GiveKudoView: Allows a user to send kudos to another user with validations.

Dependencies:
    - rest_framework
    - django.contrib.auth
    - django.shortcuts
    - django.utils.timezone
    - kudos_app.models
    - kudos_app.serializers
"""


from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from .serializers import SignupSerializer, LoginSerializer
from datetime import timedelta
from django.utils import timezone
from .models import Kudo
from .serializers import KudoSerializer, GiveKudoSerializer, UserSerializer

# Create your views here.

class HomePageView(TemplateView):
    """
    Renders the homepage of the Kudos application.
    
    Template:
        kudos_app/home.html
    """
    template_name = 'kudos_app/home.html'

class SignupView(generics.CreateAPIView):
    """
    API view for registering a new user.

    Methods:
        post: Validates and creates a new user using SignupSerializer.
    
    Permissions:
        AllowAny
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer 

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "User profile created successfully")
            return redirect('/Kudos/')
            # return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    """
    API view for logging in a user.

    Methods:
        get: Redirects authenticated users or prompts for login.
        post: Authenticates the user and starts a session.
    
    Permissions:
        AllowAny
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect('/Kudos/')
        return Response({'detail': 'Please log in by POSTing credentials.'})

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            login(request, serializer.validated_data['user'])  # uses Django session
            messages.success(request, "You are logged in successfully.")
            return redirect('/Kudos/')
            # return Response({'message': 'Login successful'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.CreateAPIView):
    """
    API view for logging out the current authenticated user.

    Methods:
        get: Logs out the user and redirects to the homepage.
    """
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('/Kudos/')
    
class MeView(generics.RetrieveAPIView):
    """
    API view to retrieve details of the currently authenticated user.

    Methods:
        get: Returns serialized user data.
    
    Permissions:
        IsAuthenticated
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class KudosReceivedView(generics.ListAPIView):
    """
    API view to list kudos received by the another user.

    Methods:
        get_queryset: Returns kudos where the current user is the receiver.
    
    Permissions:
        IsAuthenticated
    """
    serializer_class = KudoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.received_kudos.order_by('-created_at')

class KudosGivenView(generics.ListAPIView):
    """
    API view to list kudos given by the authenticated user.

    Methods:
        get_queryset: Returns kudos sent by the current user.
    
    Permissions:
        IsAuthenticated
    """
    serializer_class = KudoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Kudo.objects.filter(sender=self.request.user).order_by('-created_at')


class GiveKudoView(generics.CreateAPIView):
    """
    API view for sending kudos to another user.

    Methods:
        perform_create: Validates weekly kudo limit and organization match before saving.

    Business Rules:
        - Users can give a maximum of 3 kudos per week.
        - Users can only give kudos to others in the same organization.

    Permissions:
        IsAuthenticated
    """
    serializer_class = GiveKudoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        # Count kudos given this week
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())

        kudos_this_week = Kudo.objects.filter(
            sender=user,
            created_at__date__gte=start_of_week
        ).count()

        if kudos_this_week >= 3:
            raise serializers.ValidationError("You have already given 3 kudos this week.")

        # Validate org match again for extra safety
        receiver = serializer.validated_data.get('receiver')
        if receiver.organization != user.organization:
            raise serializers.ValidationError("Receiver must be in your organization.")

        serializer.save(sender=user)