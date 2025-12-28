from loans_project.models.loans import Loan
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils.timezone import now
from loans_project.models.loans import Loan
from loans_project.models.disbursements import Disbursments
from loans_project.models.admin import AdminUser
import uuid
from django.db import transaction
from loans_project.core.functions.logs import log_user_activity

"""
Make loan disbursements
"""

def make_disbursement(admin_id, loan_id, status):
    try:
        # check admin
        if not AdminUser.objects.filter(id=admin_id).exists():
            return {'message': 'User not authorized to perform action'}, 403

        # lock loan row
        loan = Loan.objects.select_for_update().filter(loan_id=loan_id).first()
        if not loan:
            return {'message': 'Loan application does not exist'}, 404

        # state validation
        if loan.status != "APPROVED":
            return {
                'message': f'Loan cannot be disbursed in {loan.status} state'
            }, 400

        with transaction.atomic():

            # update loan
            loan.disbursed_at = now()
            loan.save()

            # create disbursement record
            Disbursments.objects.create(
                loan=loan,
                disbursement_id=str(uuid.uuid4()),
                amount=Decimal(loan.amount),
                status=status,
                disbursed_at=loan.disbursed_at
            )

            #make logs
            log_user_activity(admin_id, 'ADMIN', f'Admin made a loan disbursement to loan:{loan_id}')

        return {'message': 'Loan disbursed successfully'}, 200

    except Exception as e:
        print(f"disbursement error: {e}")
        return {'message': 'Something went wrong'}, 500