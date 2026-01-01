from django.db import models
import uuid
from django.contrib.auth import get_user_model

class Dispute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    dispute_id = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    # Who filed the dispute
    raised_by_id = models.CharField(max_length=255)
    raised_by_type = models.CharField(
        max_length=20
    )  # USER | PROVIDER

    # Who the dispute is against
    target_id = models.CharField(max_length=255)
    target_type = models.CharField(
        max_length=20
    )  # USER | PROVIDER | PLATFORM

    # What the dispute is about
    reference_id = models.CharField(
        max_length=255, db_index=True
    )  # transaction_id, file_id, payout_id, etc.

    reference_type = models.CharField(
        max_length=50
    )  # TRANSACTION | FILE | PAYOUT | SERVICE

    dispute_type = models.CharField(max_length=100)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        default="OPEN"
    )  # OPEN | RESPONDED | RESOLVED | REJECTED

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute {self.dispute_id} ({self.status})"

class DisputeResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    dispute_id = models.CharField(max_length=100, db_index=True)

    responder_id = models.CharField(max_length=255)
    responder_type = models.CharField(
        max_length=20
    )  # USER | PROVIDER | ADMIN

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.dispute_id}"
