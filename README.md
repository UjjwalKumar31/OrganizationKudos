# 🎉 OrganizationKudos - Kudos App

A Python - Django application that allows users to give and receive Kudos within their organization. Users can send up to 3 kudos per week, fostering a culture of recognition and appreciation.

---

## 🚀 Features

- User signup, login, and logout with session-based authentication.
- Users belong to an organization and can only send kudos within their org.
- Give up to 3 kudos per week (limit enforced automatically).
- View kudos received and kudos given.
- Admin or dev command to generate demo data for testing.

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: Django sessions
- **Database**: SQLite (default, can be swapped)
- **Faker**: For generating fake demo users

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
[git clone https://github.com/your-username/kudos-app.git](https://github.com/UjjwalKumar31/OrganizationKudos.git)
```

### 2. Configuration & Environment Setup
Run the following commands in your terminal:
- git clone https://github.com/your-username/kudos-app.git
- python -m venv env          [Create a virtual environment]
- ./env/Scripts/Activate      [Windows : Activate a virtual environment]
- Inside project folder OrgKudos : pip install -r requirements.txt   [Install dependencies]
- python manage.py makemigrations      [Run initial migrations]
- python manage.py migrate
- python manage.py generate_profile    [Generate demo data (users, orgs)]
- python manage.py createsuperuser     [Create an admin user (optional)]
- python manage.py runserver           [Run the development server]
Visit the app at: http://127.0.0.1:8000/


### 🧠 Python Scripts Overview

# views.py
Defines all the core API endpoints using Django REST Framework:

HomePageView: Loads the landing page.
SignupView: Handles user registration.
LoginView: Handles login via username/password.
LogoutView: Logs out the user.
MeView: Returns the authenticated user's profile info.
KudosReceivedView: Lists kudos the user has received.
KudosGivenView: Lists kudos the user has given.
GiveKudoView: Validates and sends a new kudo (3 per week limit).

# serializers.py
Defines data validation and serialization logic:

SignupSerializer: Validates and creates new users.
LoginSerializer: Authenticates users using credentials.
KudoSerializer: Read-only view of kudos (sender, receiver, message).
GiveKudoSerializer: Validates rules for sending kudos.
UserSerializer: Displays user info and kudos left this week.

# models.py
Defines the core database models:

Organization: Represents a company or group.
User: Custom user model linked to an organization.
Kudo: Represents a kudo (sender, receiver, message, timestamp).

# urls.py
Maps HTTP endpoints to views:

| Endpoint           | Method | Description                  |
| ------------------ | ------ | ---------------------------- |
| `/signup/`         | POST   | Register a new user          |
| `/login/`          | POST   | Authenticate and log in user |
| `/logout/`         | GET    | Log out the user             |
| `/me/`             | GET    | Get current user info        |
| `/kudos/received/` | GET    | List kudos received          |
| `/kudos/given/`    | GET    | List kudos given             |
| `/kudos/give/`     | POST   | Send a new kudo              |

# generate_profile.py
A custom Django management command to generate demo data:

Clears all existing users, kudos, and organizations.
Creates sample organizations.
Creates fake users using Faker.
(Optional) Can auto-generate random kudos between users.
Run it using: python manage.py generate_profile
