from django.db import models
from django.contrib.auth import get_user_model
from models.loans import Loan
import uuid

User = get_user_model()

class Handover(models.Model):
    ESCALATION_STAGE_CHOICES = [
        ("COLLECTION", "Debt Collection"),
        ("LEGAL", "Legal Action"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("CLOSED", "Closed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="handovers")
    escalated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="escalations")
    stage = models.CharField(max_length=20, choices=ESCALATION_STAGE_CHOICES, default="COLLECTION")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")  # 🔑 New field
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # tracks last update

    def __str__(self):
        return f"Handover {self.stage} - Loan {self.loan.id} - {self.status}"