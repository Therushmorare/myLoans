from django.db import models
import uuid

class PayoutRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    payout_id = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    provider_id = models.CharField(max_length=255, db_index=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=20,
        default="PENDING"
    )  # PENDING | APPROVED | REJECTED | PAID

    processed_by = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    comments = models.TextField(
        null=True,
        blank=True
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payout {self.payout_id} - {self.status}"
