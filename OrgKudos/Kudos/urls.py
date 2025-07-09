"""
URL configuration for the Kudos application.

This module defines URL patterns for user authentication, user profile, and kudo-related views.
All views are implemented as class-based views imported from `views.py`.

Routes:
    - '' (home): Renders the homepage.
    - 'signup/': Handles user registration.
    - 'login/': Handles user login.
    - 'logout/': Logs out the authenticated user.
    - 'me/': Retrieves the current authenticated user's profile.
    - 'kudos/received/': Lists kudos received by the user.
    - 'kudos/given/': Lists kudos given by the user.
    - 'kudos/give/': Allows the user to give kudos to another user.
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('kudos/received/', KudosReceivedView.as_view(), name='kudos-received'),
    path('kudos/given/', KudosGivenView.as_view(), name='kudos-given'),
    path('kudos/give/', GiveKudoView.as_view(), name='give-kudo'),
]

