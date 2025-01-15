from django.contrib.auth.backends import BaseBackend
from .models import UserRegistration
from django.contrib.auth.hashers import check_password  # Import for password checking

class UserRegistrationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = UserRegistration.objects.get(email=email)
            # Verify the hashed password
            if check_password(password, user.password):  
                return user
        except UserRegistration.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserRegistration.objects.get(pk=user_id)
        except UserRegistration.DoesNotExist:
            return None
