from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model

class Withdrawals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id =  models.CharField(max_length=100, unique=True)
    loan_id = models.CharField(max_length=100, unique=True)
    widthdrawal_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default="PENDING")
    comments = models.TextField(max_length=500, default="NONE")
    admin_id = models.CharField(max_length=100, unique=True, default="NONE")
    created_at = models.DateTimeField(auto_now_add=True)