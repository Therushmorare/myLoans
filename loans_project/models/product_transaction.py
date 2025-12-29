from django.db import models
import uuid
from django.contrib.auth import get_user_model

class ProductTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider_id = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    item = models.CharField()
    quantity = models.IntegerField()
    description = models.TextField()
    amount = models.DecimalField()
    status = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
