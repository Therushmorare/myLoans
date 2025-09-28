from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Client(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Includes additional fields for loans app.
    """
    # Personal Info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)  # already in AbstractUser
    last_name = models.CharField(max_length=50)   # already in AbstractUser
    email = models.EmailField(unique=True)        # already in AbstractUser, enforce uniqueness
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # App-specific flags
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # can login
    is_verified = models.BooleanField(default=True)

    # Optional: timestamp
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.email})"