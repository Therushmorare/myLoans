# models.py
from django.db import models
import uuid
from decimal import Decimal

class QRPayment(models.Model):
    qr_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=100, unique=True)
    provider_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, blank=True, null=True)  # who scans
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    currency = models.CharField(max_length=10, default="ZAR")
    status = models.CharField(max_length=20, default="PENDING")  # PENDING / USED / EXPIRED
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
