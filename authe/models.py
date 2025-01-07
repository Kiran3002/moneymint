from django.db import models

from django.db import models
from django.contrib.auth.hashers import make_password


class UserRegistration(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    first_name = models.CharField(max_length=150)  # First name field
    email = models.EmailField(unique=True)  # Email as the unique identifier
    date_of_birth = models.DateField()  # Date of birth field
    aadhar = models.CharField(max_length=12, unique=True)  # Aadhar card number
    pancard = models.CharField(max_length=10, unique=True)  # PAN card number
    password = models.CharField(max_length=128)  # Hashed password
    address = models.TextField()  # Address field
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # User role
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of registration
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    def set_password(self, raw_password):
        """
        Hashes the raw password and saves it to the password field.
        """
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.first_name} ({self.email})"
