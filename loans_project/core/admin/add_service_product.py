import uuid
from django.db import transaction
from loans_project.models.admin import AdminUser
from loans_project.models.loan_packages import LoanPackage

"""
Add a new service product
"""

def add_new_service(admin_id, service_name, description, percentage, duration, offering_amount):
    try:
        admin = AdminUser.objects.filter(id=admin_id, is_active=True).first()

        if not admin:
            return {'message': 'User does not have permission to perform this action'}, 403

        if any(x in [None, ""] for x in [service_name, description, percentage, duration, offering_amount]):
            return {'message': 'Please fill out all required fields'}, 400

        if percentage <= 0 or duration <= 0 or offering_amount <= 0:
            return {'message': 'Invalid service values provided'}, 400

        if LoanPackage.objects.filter(service_name__iexact=service_name).exists():
            return {'message': 'Loan/Credit package already exists'}, 400

        with transaction.atomic():
            package = LoanPackage.objects.create(
                id=uuid.uuid4(),
                admin_id=admin_id,
                service_name=service_name.strip(),
                description=description.strip(),
                percentage=percentage,
                duration=duration,
                amount=offering_amount,
                status='PENDING'
            )

        return {
            'message': 'Loan/Credit product added successfully',
            'package_id': str(package.id),
            'status': package.status,
            'service_name': package.service_name,
            'description': package.description,
            'percentage': package.percentage,
            'duration': package.duration,
            'amount': package.amount
        }, 201

    except Exception as e:
        print(f'Credit Product Error: {e}')
        return {'message': 'Something went wrong'}, 500
