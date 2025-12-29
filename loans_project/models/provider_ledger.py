from django.db import models
import uuid

class ProviderLedger(models.Model):
    ENTRY_TYPES = (
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    )

    SOURCES = (
        ("QR_PAYMENT", "QR Payment"),
        ("MANUAL_ADJUSTMENT", "Manual Adjustment"),
        ("MONTHLY_PAYOUT", "Monthly Payout"),
        ("REVERSAL", "Reversal"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    provider_id = models.CharField(max_length=100, db_index=True)

    reference_id = models.CharField(
        max_length=100,
        help_text="Transaction ID, payout batch ID, or reversal reference"
    )

    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPES
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCES
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["provider_id", "created_at"]),
            models.Index(fields=["reference_id"]),
        ]

    def __str__(self):
        return f"{self.provider_id} | {self.entry_type} | {self.amount}"
