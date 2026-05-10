from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    # Role Choices
    ROLE_CHOICES = (
        ('INSTRUCTOR', 'Instructor'),
        ('STUDENT', 'Student'),
        ('ADMIN', 'Admin'),
    )

    # Payout Choices
    PAYOUT_CHOICES = (
        ('PAYPAL', 'PayPal'),
        ('INSTAPAY', 'InstaPay'),
        ('VODAFONE_CASH', 'Vodafone Cash'),
    )

    username = None # Remove the default username field
    email = models.EmailField('email address', unique=True)
    
    # Custom Fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    subdomain = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="Used for instructor tenant routing")
    
    # Financial fields for instructors
    payout_method = models.CharField(max_length=20, choices=PAYOUT_CHOICES, null=True, blank=True)
    payout_details = models.TextField(null=True, blank=True, help_text="Email or account number for payouts")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default

    objects = CustomUserManager()

    def __str__(self):
        return self.email