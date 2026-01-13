from django.db import transaction
from django.utils import timezone
from loans_project.models.admin import AdminUser
from loans_project.models.client import Client
from loans_project.models.user_manager import *
from loans_project.models.service_provider import ServiceProvider
from loans_project.core.functions.logs import log_user_activity

"""
Delete Users
"""

def delete_user(admin_id, user_id):
    try:
        # Check if admin exists
        admin = AdminUser.objects.filter(id=admin_id).first()
        if not admin:
            return {'message': 'User does not have permission to perform this action!'}, 403

        # Find the user in Client, ServiceProvider, or AdminUser
        user = Client.objects.filter(id=user_id).first() or \
               ServiceProvider.objects.filter(id=user_id).first() or \
               AdminUser.objects.filter(id=user_id).first()

        if not user:
            return {'message': 'User does not exist'}, 404

        # Delete the user instance
        user.delete()

        # Log action
        log_user_activity(
            admin_id,
            "ADMIN",
            f"Deleted User: {user_id}"
        )

        return {'message': 'User deleted successfully'}, 200

    except Exception as e:
        print(f"User Delete Error: {e}")
        return {'message': 'Something went wrong'}, 500
