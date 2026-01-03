
from loans_project.models.admin import AdminUser
from loans_project.models.loan_packages import LoanPackage

"""
Delete loan package
"""
def delete_loan_package(admin_id, package_id):
    try:
        admin = AdminUser.objects.filter(id=admin_id).first()
        if not admin:
            return {'message': 'User not authorized to perform this action'}, 403

        package = LoanPackage.objects.filter(id=package_id).first()
        if not package:
            return {'message': 'Loan package does not exist'}, 404

        package.delete()

        return {'message': 'Loan package deleted successfully'}, 200

    except Exception as e:
        print(f"Package delete error: {e}")
        return {'message': 'Something went wrong'}, 500
