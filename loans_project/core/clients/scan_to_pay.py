from loans_project.models.service_provider import ServiceProvider
import uuid
from loans_project.models.product_transaction import ProductTransaction
from decimal import Decimal
from django.db import transaction
from loans_project.utils.qr import generate_qr_base64
from loans_project.models.qr_code import QRPayment
from datetime import timedelta
from django.utils import timezone
from loans_project.core.functions.cdn_file_upload import file_upload
from loans_project.models.client_wallet import Wallet
from loans_project.models.provider_ledger import ProviderLedger
from loans_project.models.processed_transactions import ProcessedTransactions

"""
Scan QR code and pay
"""

def redeem_qr_payment(request):
    transaction_id = request.POST.get("transaction_id")
    item_id = request.POST.get("item_id")
    user_id = request.POST.get("user_id")

    if not all([transaction_id, item_id, user_id]):
        return {'message': 'Missing required fields'}, 400

    with transaction.atomic():

        # Lock QR
        qr = QRPayment.objects.select_for_update().filter(
            transaction_id=transaction_id,
            status="PENDING"
        ).first()

        if not qr:
            return {'message': 'Invalid or already used QR'}, 400

        if qr.expires_at < timezone.now():
            qr.status = "EXPIRED"
            qr.save(update_fields=["status"])
            return {'message': 'QR expired'}, 400

        # Lock wallet
        wallet = Wallet.objects.select_for_update().filter(
            user_id=user_id
        ).first()

        if not wallet or wallet.balance < qr.amount:
            ProcessedTransactions.objects.create(
                transaction_id=transaction_id,
                item_id=item_id,
                user_id=user_id,
                status='DECLINED',
                reasons='Insufficient balance'
            )
            return {'message': 'Insufficient balance'}, 400

        # Debit wallet
        wallet.balance -= Decimal(qr.amount)
        wallet.save(update_fields=["balance"])

        # Credit provider ledger (IMMUTABLE)
        ProviderLedger.objects.create(
            provider_id=qr.provider_id,
            reference_id=transaction_id,
            entry_type="CREDIT",
            source="QR_PAYMENT",
            amount=qr.amount,
            description=f"QR payment by user {user_id}"
        )

        # Mark product transaction as paid
        ProductTransaction.objects.filter(
            transaction_id=transaction_id,
            status="PENDING"
        ).update(status="PAID")

        # Record processed transaction
        ProcessedTransactions.objects.create(
            transaction_id=transaction_id,
            item_id=item_id,
            user_id=user_id,
            status='PAID',
            reasons='QR payment settled'
        )

        # Consume QR
        qr.status = "USED"
        qr.user_id = user_id
        qr.used_at = timezone.now()
        qr.save(update_fields=["status", "user_id", "used_at"])

    return {
        'message': 'Payment successful',
        'transaction_id': transaction_id
    }, 200