from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

class UserRegistration(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    aadhar = models.CharField(max_length=12)
    pancard = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    address = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)  # New field
    funds = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aadhar', 'pancard'], name='unique_aadhar_pancard')
        ]

    def set_password(self, raw_password):
        """
        Hashes the raw password and saves it to the password field.
        """
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"{self.first_name} ({self.email})"
