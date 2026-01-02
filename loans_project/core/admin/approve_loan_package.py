from loans_project.models.admin import AdminUser
from loans_project.models.loan_packages import LoanPackage

"""
Loan package approval or reject method
"""

def approve_or_reject_loan_package(admin_id, package_id, status, comments=None):
    try:
        admin = AdminUser.objects.filter(id=admin_id, is_active=True).first()
        if not admin:
            return {'message': 'User not authorized'}, 403

        if status not in ['APPROVED', 'REJECTED']:
            return {'message': 'Invalid status'}, 400

        package = LoanPackage.objects.filter(id=package_id).first()
        if not package:
            return {'message': 'Loan package does not exist'}, 404

        if package.status != 'PENDING':
            return {'message': 'Loan package already processed'}, 400

        package.status = status
        if comments:
            package.comments = comments

        package.approved_by = admin_id
        package.save()

        return {
            'message': f'Loan package {status.lower()} successfully',
            'package_id': package_id,
            'status': status
        }, 200

    except Exception as e:
        print(f"Loan Package Approval Error: {e}")
        return {'message': 'Something went wrong'}, 500
