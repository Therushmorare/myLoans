from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class MFA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user_id = models.CharField(max_length=255, db_index=True)
    user_type = models.CharField(
        max_length=50,
        db_index=True
    )  # ADMIN, PROVIDER, CLIENT

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["user_id", "user_type"]),
            models.Index(fields=["code"]),
        ]

    def is_expired(self):
        return timezone.now() > self.expires_at

    def mark_verified(self):
        self.verified = True
        self.save(update_fields=["verified"])

    def __str__(self):
        return f"MFA {self.user_type} | {self.user_id} | Verified={self.verified}"
