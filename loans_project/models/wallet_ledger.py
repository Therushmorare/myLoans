from django.db import models
import uuid
from decimal import Decimal

class WalletLedger(models.Model):


    ENTRY_TYPES = (
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    )

    SOURCES = (
        ("LOAN_DISBURSEMENT", "Loan Disbursement"),
        ("WITHDRAWAL_REQUEST", "Withdrawal Request"),
        ("WITHDRAWAL_APPROVED", "Withdrawal Approved"),
        ("WITHDRAWAL_REVERSAL", "Withdrawal Reversal"),
        ("QR_PAYMENT", "QR Payment"),
        ("MANUAL_PAYMENT", "Manual Payment"),
        ("REFUND", "Refund"),
        ("ADJUSTMENT", "Adjustment"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    user_id = models.CharField(max_length=100, db_index=True)
    reference_id = models.CharField(max_length=100, help_text="External reference (withdrawal_id, transaction_id, etc.)", db_index=True)
    entry_type = models.CharField(max_length=10,choices=ENTRY_TYPES)
    source = models.CharField(max_length=50,choices=SOURCES)
    amount = models.DecimalField(max_digits=14,decimal_places=2)
    balance_snapshot = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True,help_text="Wallet balance after this transaction")
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["reference_id"]),
        ]

    def __str__(self):
        return f"{self.user_id} | {self.entry_type} | {self.amount}"
