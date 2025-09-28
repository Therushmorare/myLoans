from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")

    # loan details
    loan_id = models.CharField(max_length=100, unique=True)  # external reference
    package = models.CharField(max_length=100)               # e.g. "Payday Loan"
    loan_term = models.CharField(max_length=50)              # short/mid/long term
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # %
    duration_months = models.IntegerField()                  # months
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="PENDING")

    # applicant details (snapshot at application time)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    citizen = models.BooleanField(default=True)
    id_number = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)

    # employment details
    company = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # file uploads
    id_document = models.FileField(upload_to="documents/id/")
    proof_of_income = models.FileField(upload_to="documents/income/")
    proof_of_residence = models.FileField(upload_to="documents/residence/")
    employment_doc = models.FileField(upload_to="documents/employment/")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.loan_id} ({self.status})"