from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("DEFAULTED", "Defaulted"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    loan_type = models.CharField(max_length=100)
    loan_duration = models.CharField(max_length=50)   # e.g. "30 days"
    loan_interest = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 12.5 (%)
    amount = models.DecimalField(max_digits=12, decimal_places=2)        # precise amount
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default="PENDING")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.status})"