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

"""
Create payable transaction
"""

def create_transaction(provider_id, item_name, quantity, amount, description, item_id):
    try:
        provider = ServiceProvider.objects.filter(provider_id=provider_id).first()
        if not provider:
            return {'message': 'Service provider does not exist'}, 404

        if any(x is None for x in [item_name, quantity, amount, description, item_id]):
            return {'message': 'Please fill out all inputs'}, 400

        try:
            quantity = int(quantity)
            unit_amount = Decimal(amount)
        except Exception:
            return {'message': 'Invalid quantity or amount'}, 400

        if quantity <= 0 or unit_amount <= 0:
            return {'message': 'Quantity and amount must be greater than zero'}, 400

        with transaction.atomic():
            transaction_id = str(uuid.uuid4())

            subtotal = unit_amount * Decimal(quantity)
            vat = subtotal * Decimal("0.15")
            total_payable = subtotal + vat

            product_txn = ProductTransaction.objects.create(
                provider_id=provider_id,
                transaction_id=transaction_id,
                item_id=item_id,
                item=item_name,
                quantity=quantity,
                description=description,
                amount=total_payable,
                status='PENDING'
            )

            expires_at = timezone.now() + timedelta(hours=2)

            qr_payment = QRPayment.objects.create(
                transaction_id=transaction_id,
                provider_id=provider_id,
                amount=total_payable,
                status="PENDING",
                expires_at=expires_at
            )

        qr_payload = {
            "transaction_id": transaction_id,
            "provider_id": provider_id,
            "amount": str(total_payable),
            "currency": "ZAR",
            "expires_at": expires_at.isoformat()
        }

        qr_base64 = generate_qr_base64(qr_payload)
        qr_url = file_upload(qr_base64, f"qr_{transaction_id}")

        return {
            'message': 'Transaction created successfully',
            'transaction': {
                'transaction_id': transaction_id,
                'provider_id': provider_id,
                'item_id': item_id,
                'item': item_name,
                'quantity': quantity,
                'description': description,
                'subtotal': str(subtotal),
                'vat': str(vat),
                'total_payable': str(total_payable),
                'status': product_txn.status,
                'qr_url': qr_url
            }
        }, 200

    except Exception as e:
        print(f"Create transaction error: {e}")
        return {'message': 'Something went wrong'}, 500