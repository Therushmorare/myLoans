from loans_project.models.admin import AdminUser
import uuid
from django.db import transaction
from loans_project.core.functions.logs import log_user_activity
from loans_project.models.service_provider import ServiceProvider
from loans_project.core.functions.string_gen import generate_random_string
from loans_project.email_sender.mail_helpers import send_credentials_email

"""
Add new admin
"""

def add_new_admin(admin_id, first_name, last_name, email, phone_number, role):
    try:
        # Verify requesting admin
        requesting_admin = AdminUser.objects.filter(id=admin_id, is_active=True).first()
        if not requesting_admin:
            return {'message': 'User not authorized'}, 403

        if any(x is None for x in [first_name, last_name, email, phone_number, role]):
            return {'message': 'Please fill out all credentials'}, 400

        if AdminUser.objects.filter(email=email).exists():
            return {'message': 'Admin with this email already exists'}, 400

        password = generate_random_string(10)

        with transaction.atomic():
            new_admin = AdminUser.objects.create(
                email=email,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                role=role,
                is_verified=True
            )
            new_admin.set_password(password)  #hash password
            new_admin.save()

        # Send credentials
        send_credentials_email(email, password)

        # Log action
        log_user_activity(
            admin_id,
            "ADMIN",
            f"Created admin user {new_admin.id}"
        )

        return {
            'message': 'Admin added successfully',
            'admin_id': new_admin.id,
            'email': email,
            'role': role
        }, 200

    except Exception as e:
        print(f"Add new admin error: {e}")
        return {'message': 'Something went wrong'}, 500