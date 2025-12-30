import uuid
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from loans_project.models.client_wallet import Wallet
from loans_project.models.loans import Loan
from loans_project.models.disbursements import Disbursments
from loans_project.models.client import Client
from loans_project.models.withdrawal_requests import Withdrawals

"""
Request Withdrawal
"""

def request_withdrawal(user_id, loan_id):
    try:
        with transaction.atomic():

            client = Client.objects.filter(id=user_id).first()
            if not client:
                return {'message': 'User does not exist'}, 404

            loan = Loan.objects.filter(
                loan_id=loan_id,
                user=client,
                status="APPROVED"
            ).first()

            if not loan:
                return {'message': 'Loan not approved or does not exist'}, 404

            #Lock wallet
            wallet = Wallet.objects.select_for_update().filter(
                user_id=user_id
            ).first()

            if not wallet:
                return {'message': 'Add a wallet to request a withdrawal'}, 404

            #Lock disbursement
            disbursement = Disbursments.objects.select_for_update().filter(
                loan_id=loan_id,
                status="AVAILABLE"
            ).first()

            if not disbursement:
                return {'message': 'No available disbursement for this loan'}, 400

            if wallet.balance < disbursement.amount:
                return {'message': 'Insufficient balance'}, 400

            #Debit wallet
            wallet.balance -= Decimal(disbursement.amount)
            wallet.save(update_fields=["balance"])

            # Create withdrawal request
            withdrawal_id = str(uuid.uuid4())

            withdrawal = Withdrawals.objects.create(
                user_id=user_id,
                loan_id=loan_id,
                widthdrawal_id=withdrawal_id,
                amount=disbursement.amount,
                status='PENDING'
            )

            return {
                'message': 'Withdrawal request submitted successfully',
                'withdrawal_id': withdrawal_id,
                'amount': str(disbursement.amount),
                'loan_id': loan_id,
                'wallet_balance': str(wallet.balance)
            }, 200

    except Exception as e:
        print(f"Withdrawal Error: {e}")
        return {'message': 'Something went wrong'}, 500