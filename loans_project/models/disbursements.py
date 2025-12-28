from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model

class Disbursments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan_id = models.CharField(max_length=100, unique=True)
    disbursement_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default="APPROVED")
    created_at = models.DateTimeField(auto_now_add=True)