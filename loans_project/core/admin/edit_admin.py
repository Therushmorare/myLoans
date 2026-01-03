from loans_project.models.admin import AdminUser
import uuid
from django.db import transaction
from loans_project.core.functions.logs import log_user_activity
from loans_project.core.functions.string_gen import generate_random_string
from loans_project.email_sender.mail_helpers import send_credentials_email

"""
Edit admin user details
"""

def edit_admin(requesting_admin_id, admin_id, first_name=None, last_name=None, email=None, phone_number=None, role=None):
    try:
        # Verify requesting admin
        requesting_admin = AdminUser.objects.filter(id=requesting_admin_id).first()

        if not requesting_admin:
            return {'message': 'User not authorized'}, 403

        # Lock admin record
        admin = AdminUser.objects.select_for_update().filter(id=admin_id).first()

        if not admin:
            return {'message': 'Admin does not exist'}, 404

        with transaction.atomic():

            # Email uniqueness (exclude self)
            if email and AdminUser.objects.filter(email=email).exclude(id=admin_id).exists():
                return {'message': 'Email already in use'}, 400

            if first_name:
                admin.first_name = first_name

            if last_name:
                admin.last_name = last_name

            if email:
                admin.email = email

            if phone_number:
                admin.phone_number = phone_number

            if role:
                admin.role = role

            admin.save()

        # Log action
        log_user_activity(
            requesting_admin_id,
            "ADMIN",
            f"Updated admin user {admin_id}"
        )

        return {
            'message': 'Admin updated successfully',
            'admin_id': admin_id
        }, 200

    except Exception as e:
        print(f"Edit admin error: {e}")
        return {'message': 'Something went wrong'}, 500
