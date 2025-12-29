from django.db import models
import uuid
from django.contrib.auth import get_user_model

class ProcessedTransactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=100)
    transaction_type = models.CharField()
    item_id = models.CharField()
    user_id = models.CharField()
    status = models.CharField()
    reasons = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

