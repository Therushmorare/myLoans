from django.db import models
from django.contrib.auth import get_user_model
from .loans import Loan
import uuid

User = get_user_model()

class UserLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interests")
    action = models.CharField()
    user_type = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)