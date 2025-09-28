from django.db import models
from django.contrib.auth import get_user_model
from .loans import Loan
import uuid

User = get_user_model()

class Repayment(models.Model):
    REPAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="repayments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=REPAYMENT_STATUS_CHOICES, default="PENDING")
    repaid_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=255, blank=True, null=True)  # e.g. payment gateway ref

    def __str__(self):
        return f"Repayment {self.id} - Loan {self.loan.id} - {self.amount}"