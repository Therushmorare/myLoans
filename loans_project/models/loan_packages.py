import uuid
from django.db import models

class LoanPackage(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('DISABLED', 'Disabled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Admin who created the package
    admin = models.ForeignKey(
        'AdminUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_loan_packages'
    )

    service_name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )

    description = models.TextField()

    # Financials
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Interest or service percentage"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Maximum offering amount"
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in days"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    is_active = models.BooleanField(default=False)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'loan_packages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['is_active']),
        ]

    def activate(self):
        self.status = 'ACTIVE'
        self.is_active = True
        self.save(update_fields=['status', 'is_active'])

    def suspend(self):
        self.status = 'SUSPENDED'
        self.is_active = False
        self.save(update_fields=['status', 'is_active'])

    def disable(self):
        self.status = 'DISABLED'
        self.is_active = False
        self.save(update_fields=['status', 'is_active'])

    def __str__(self):
        return f"{self.service_name} ({self.status})"
