from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ServiceProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    added_by = models.CharField(max_length=100, unique=True)
    provider_id = models.CharField(max_length=100, unique=True)
    provider_name = models.CharField()
    email = models.CharField()
    phone = models.CharField()
    type = models.CharField()
    address = models.TextField()
    password = models.CharField()
    status = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)