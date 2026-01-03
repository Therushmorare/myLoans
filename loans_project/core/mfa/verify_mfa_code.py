from datetime import timezone, datetime
from django.utils import timezone as dj_timezone
from django.db import transaction
from loans_project.models.mfa import MFA

def verify_mfa_code(user_id, code):
    """
    Verify an MFA code for a given user.
    Returns (bool, message)
    """
    try:
        # Lock row for update in case multiple requests come at the same time
        with transaction.atomic():
            mfa_record = MFA.objects.select_for_update().filter(
                user_id=user_id,
                code=code,
                verified=False
            ).first()

            if not mfa_record:
                return False, "Invalid code"

            # Check expiry
            if mfa_record.expires_at < dj_timezone.now():
                return False, "Code expired"

            # Mark verified
            mfa_record.verified = True
            mfa_record.save(update_fields=["verified"])

        return True, "Code verified successfully"

    except Exception as e:
        print(f"MFA verification error: {e}")
        return False, "Something went wrong"
