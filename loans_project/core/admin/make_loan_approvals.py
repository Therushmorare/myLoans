from loans_project.models.loans import Loan
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils.timezone import now
from loans_project.models.loans import Loan
from loans_project.models.admin import AdminUser
import uuid
from django.db import transaction
from loans_project.core.functions.logs import log_user_activity

"""
Loan application status updater
"""

def loan_approvals(admin_id, loan_id, status):
    try:
        #check admin
        if not AdminUser.objects.filter(id=admin_id).exists():
            return {'message': 'User not authorized to perform action'}, 403
        
        # lock loan row
        loan = Loan.objects.select_for_update().filter(loan_id=loan_id).first()
        if not loan:
            return {'message': 'Loan application does not exist'}, 404
        
        if loan.status == "APPROVED":
            return {
                'message': f'Loan is already approved'
            }, 400
        
        with transaction.atomic():
            loan.status = status
            loan.save()

        log_user_activity(admin_id, 'ADMIN', f'Admin user approved loan:{loan_id}')
        
        return {'message': 'Loan status approved successfully'}, 200
    
    except Exception as e:
        print(f"Loan status error:{e}")
        return {'message': 'Something went wrong'}, 500