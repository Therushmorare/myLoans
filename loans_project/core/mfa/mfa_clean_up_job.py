from django.utils import timezone
from loans_project.models.mfa import MFA

def cleanup_expired_mfa_codes():
    expired_codes = MFA.objects.filter(
        expires_at__lt=timezone.now(),
        verified=False
    )

    deleted_count, _ = expired_codes.delete()
    return deleted_count
