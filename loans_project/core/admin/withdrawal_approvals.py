from django.db import transaction
from decimal import Decimal
from django.utils import timezone

from loans_project.models.admin import AdminUser
from loans_project.models.client_wallet import Wallet
from loans_project.models.withdrawal_requests import Withdrawals
from loans_project.models.wallet_ledger import WalletLedger
from loans_project.core.functions.logs import log_user_activity

"""
Admin approves or rejects withdrawals
"""

def withdrawal_approve_reject(withdrawal_id, admin_id, status, comments):
    try:
        if status not in ["APPROVED", "REJECTED"]:
            return {'message': 'Invalid status'}, 400

        with transaction.atomic():

            #Validate admin
            admin = AdminUser.objects.filter(id=admin_id).first()
            if not admin:
                return {'message': 'User not authorized'}, 403

            #Lock withdrawal
            withdrawal = Withdrawals.objects.select_for_update().filter(
                widthdrawal_id=withdrawal_id
            ).first()

            if not withdrawal:
                return {'message': 'Withdrawal does not exist'}, 404

            if withdrawal.status != "PENDING":
                return {
                    'message': f'Withdrawal already {withdrawal.status.lower()}'
                }, 400

            #Update withdrawal status
            withdrawal.status = status
            withdrawal.comments = comments
            withdrawal.admin_id = str(admin_id)
            withdrawal.processed_at = timezone.now()
            withdrawal.save(update_fields=[
                "status", "comments", "admin_id", "processed_at"
            ])

            # Rejection refund wallet
            if status == "REJECTED":

                wallet = Wallet.objects.select_for_update().filter(
                    user_id=withdrawal.user_id
                ).first()

                if not wallet:
                    raise Exception("Wallet missing during withdrawal reversal")

                wallet.balance += Decimal(withdrawal.amount)
                wallet.save(update_fields=["balance"])

                WalletLedger.objects.create(
                    user_id=withdrawal.user_id,
                    reference_id=withdrawal_id,
                    entry_type="CREDIT",
                    source="WITHDRAWAL_REVERSAL",
                    amount=withdrawal.amount,
                    balance_snapshot=wallet.balance,
                    description="Withdrawal rejected – funds returned"
                )

            # Approval funds leave platform (payout later)
            if status == "APPROVED":
                WalletLedger.objects.create(
                    user_id=withdrawal.user_id,
                    reference_id=withdrawal_id,
                    entry_type="DEBIT",
                    source="WITHDRAWAL_APPROVED",
                    amount=withdrawal.amount,
                    balance_snapshot=None,
                    description="Withdrawal approved for payout"
                )

            # Log action
            log_user_activity(
                admin_id,
                "ADMIN",
                f"{status} withdrawal with this ID:{withdrawal_id}"
            )

            return {
                'message': f'Withdrawal {status.lower()} successfully',
                'withdrawal_id': withdrawal_id,
                'status': status,
                'comments': comments
            }, 200

    except Exception as e:
        print(f'Withdrawal Status Update Error: {e}')
        return {'message': 'Something went wrong'}, 500
