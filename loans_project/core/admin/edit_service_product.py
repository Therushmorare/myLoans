import uuid
from django.db import transaction
from loans_project.models.admin import AdminUser
from loans_project.models.loan_packages import LoanPackage

"""
Edit service product
"""

def edit_service_product(admin_id, package_id, service_name=None, description=None, percentage=None, duration=None, offering_amount=None):
    try:
        admin = AdminUser.objects.filter(id=admin_id).first()
        if not admin:
            return {'message': 'User does not have permission to perform this action'}, 403

        package = LoanPackage.objects.filter(id=package_id).first()
        if not package:
            return {'message': 'Loan package does not exist'}, 404

        with transaction.atomic():
            if service_name is not None:
                # prevent duplicates
                if LoanPackage.objects.filter(service_name=service_name).exclude(id=package_id).exists():
                    return {'message': 'Service name already exists'}, 400
                package.service_name = service_name

            if description is not None:
                package.description = description

            if percentage is not None:
                package.percentage = percentage

            if duration is not None:
                package.duration = duration

            if offering_amount is not None:
                package.amount = offering_amount

            package.save()

        return {'message': 'Loan package updated successfully'}, 200

    except Exception as e:
        print(f"Credit Product Update Error: {e}")
        return {'message': 'Something went wrong'}, 500