import random
from datetime import timedelta
from django.utils import timezone
from loans_project.models.mfa import MFA


def generate_mfa_code(length=6):
    """Generate numeric MFA code"""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def save_mfa_code(user_id, user_type, code=None, ttl_minutes=10):
    """
    Save MFA code in DB with expiry
    """
    if not code:
        code = generate_mfa_code()

    expires_at = timezone.now() + timedelta(minutes=ttl_minutes)

    MFA.objects.create(
        user_id=str(user_id),
        user_type=user_type,
        code=code,
        expires_at=expires_at,
        verified=False
    )

    return code