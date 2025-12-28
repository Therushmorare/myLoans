from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ProviderFiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    added_by = models.CharField(max_length=100)
    provider_id = models.CharField(max_length=100)
    
    file_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True  #ensures each file has its own ID
    )

    document = models.TextField()  # safer for URLs
    uploaded_at = models.DateTimeField(auto_now_add=True)  # optional but useful
