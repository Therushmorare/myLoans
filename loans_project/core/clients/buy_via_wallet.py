from loans_project.models.product_transaction import ProductTransaction
from loans_project.models.client import Client
from loans_project.models.client_wallet import Wallet
from loans_project.models.provider_ledger import ProviderLedger
from loans_project.models.processed_transactions import ProcessedTransactions
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

"""
Pay for products manully using the transaction code
"""

def manual_pay(user_id, transaction_id):
    try:
        with transaction.atomic():

            # Lock transaction
            txn = ProductTransaction.objects.select_for_update().filter(
                transaction_id=transaction_id
            ).first()

            if not txn:
                return {'message': 'Transaction does not exist'}, 404

            if txn.status != "PENDING":
                return {
                    'message': f'Transaction already {txn.status.lower()}'
                }, 400

            user = Client.objects.filter(id=user_id).first()
            if not user:
                return {'message': 'User does not exist'}, 404

            # Lock wallet
            wallet = Wallet.objects.select_for_update().filter(
                user_id=user_id
            ).first()

            if not wallet or wallet.balance < txn.amount:
                ProcessedTransactions.objects.create(
                    transaction_id=txn.transaction_id,
                    item_id=txn.item_id,
                    user_id=user_id,
                    status='DECLINED',
                    reasons='Insufficient balance'
                )
                return {'message': 'Insufficient balance'}, 400

            # Debit wallet
            wallet.balance -= Decimal(txn.amount)
            wallet.save(update_fields=["balance"])

            # Credit provider ledger (IMMUTABLE)
            ProviderLedger.objects.create(
                provider_id=txn.provider_id,
                reference_id=transaction_id,
                entry_type="CREDIT",
                source="MANUAL_PAYMENT",
                amount=txn.amount,
                description=f"Manual payment by user {user_id}"
            )

            # Mark transaction as PAID
            txn.status = "PAID"
            txn.paid_at = timezone.now()
            txn.save(update_fields=["status", "paid_at"])

            # Record processed transaction
            ProcessedTransactions.objects.create(
                transaction_id=txn.transaction_id,
                item_id=txn.item_id,
                user_id=user_id,
                status='PAID',
                reasons='Manual payment settled'
            )

            return {
                'message': 'Payment successful',
                'transaction_id': transaction_id,
                'amount_paid': str(txn.amount)
            }, 200

    except Exception as e:
        print(f"Manual Pay Error: {e}")
        return {'message': 'Something went wrong'}, 500