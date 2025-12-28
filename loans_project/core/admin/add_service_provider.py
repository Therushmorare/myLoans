
from loans_project.models.disbursements import Disbursments
from loans_project.models.admin import AdminUser
import uuid
from django.db import transaction
from loans_project.core.functions.logs import log_user_activity
from loans_project.models.service_provider import ServiceProvider

"""
Add a new service provider
"""
def add_service_provider(admin_id, provider_name, email, phone, provider_type, address):
    try:
        # validate admin
        admin = AdminUser.objects.filter(id=admin_id).first()
        if not admin:
            return {
                "status": "failed",
                "message": "You are not authorized to perform this action"
            }, 403

        # validate inputs
        if any(x in [None, ""] for x in [provider_name, email, phone, provider_type, address]):
            return {
                "status": "failed",
                "message": "All fields are required"
            }, 400

        # prevent duplicates
        if ServiceProvider.objects.filter(email=email).exists():
            return {
                "status": "failed",
                "message": "A service provider with this email already exists"
            }, 400

        provider_id = str(uuid.uuid4())

        with transaction.atomic():
            provider = ServiceProvider.objects.create(
                added_by=admin,
                provider_id=provider_id,
                provider_name=provider_name,
                email=email,
                phone=phone,
                provider_type=provider_type,
                address=address,
                status="PENDING"
            )

            log_user_activity(
                admin_id,
                "ADMIN",
                f"Added new service provider: {provider_id}"
            )

        # informative response
        return {
            "message": "Service provider added successfully",
            "provider": {
                "provider_id": provider.provider_id,
                "provider_name": provider.provider_name,
                "email": provider.email,
                "phone": provider.phone,
                "provider_type": provider.provider_type,
                "address": provider.address,
                "added_by": admin.email
            }
        }, 200

    except Exception as e:
        print(f"Service Provider Add Error: {e}")
        return {
            "status": "error",
            "message": "An unexpected error occurred while adding the service provider"
        }, 500