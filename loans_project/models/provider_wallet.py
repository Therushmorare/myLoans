from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class ProviderWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    provider_id = models.CharField(max_length=100, unique=True)
    bank = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)

    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    status = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["provider_id"]),
            models.Index(fields=["account_number"]),
        ]

    def __str__(self):
        return f"{self.provider_id} - {self.bank} ({self.account_number})"