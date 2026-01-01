from django.db import models
import uuid

class BannedUsers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    banned_by = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banned: {self.user_id} by {self.banned_by}"


class SuspendedUsers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    suspended_by = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suspended: {self.user_id} by {self.suspended_by}"
