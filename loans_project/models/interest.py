from django.db import models
from django.contrib.auth import get_user_model
from .loans import Loan
import uuid

User = get_user_model()

class Interest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interests")
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="interests")
    incurred_amount = models.DecimalField(max_digits=12, decimal_places=2)
    incurred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.loan.user.email} - {self.incurred_amount} ({self.incurred_at.date()})"