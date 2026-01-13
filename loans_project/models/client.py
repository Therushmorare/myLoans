from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Client(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"  # <-- use email for authentication
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]  # username is still required by AbstractUser

    def __str__(self):
        return f"{self.email}"