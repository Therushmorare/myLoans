from django.db import transaction
from django.utils import timezone
from loans_project.models.admin import AdminUser
from loans_project.models.client import Client
from loans_project.models.user_manager import *
from loans_project.models.service_provider import ServiceProvider

"""
Admin manages users
"""

def manage_users(admin_id, user_id, status, comments=None):
    try:
        if status not in ["BANNED", "SUSPENDED"]:
            return {'message': 'Invalid status action'}, 400

        admin = AdminUser.objects.filter(id=admin_id).first()
        if not admin:
            return {'message': 'User not authorized to perform action'}, 403

        # Identify user type
        user = ServiceProvider.objects.filter(id=user_id).first()
        user_type = "PROVIDER"

        if not user:
            user = Client.objects.filter(id=user_id).first()
            user_type = "CLIENT"

        if not user:
            return {'message': 'User does not exist'}, 404

        # Prevent duplicate actions
        if user.status == status:
            return {
                'message': f'User is already {status.lower()}'
            }, 400

        with transaction.atomic():

            # Update user status
            user.status = status
            user.save(update_fields=["status"])

            if status == "BANNED":
                BannedUsers.objects.create(
                    banned_by=str(admin_id),
                    user_id=str(user_id),
                    user_type=user_type,
                    comments=comments,
                    created_at=timezone.now()
                )

            elif status == "SUSPENDED":
                SuspendedUsers.objects.create(
                    suspended_by=str(admin_id),
                    user_id=str(user_id),
                    user_type=user_type,
                    comments=comments,
                    created_at=timezone.now()
                )

        return {
            'message': f'User {status.lower()} successfully',
            'user_id': str(user_id),
            'user_type': user_type,
            'status': status,
            'comments': comments
        }, 200

    except Exception as e:
        print(f"User management error: {e}")
        return {'message': 'Something went wrong'}, 500
