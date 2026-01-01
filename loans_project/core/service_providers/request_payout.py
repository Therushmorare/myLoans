from django.db import transaction
from decimal import Decimal
import uuid
from loans_project.models.service_provider import ServiceProvider
from loans_project.models.provider_ledger import ProviderLedger
from loans_project.models.provider_wallet import ProviderWallet
from loans_project.models.payout import PayoutRequest

def request_payout(provider_id, amount):
    try:
        amount = Decimal(amount)

        if amount <= 0:
            return {'message': 'Invalid payout amount'}, 400

        with transaction.atomic():

            provider = ServiceProvider.objects.filter(
                provider_id=provider_id
            ).first()

            if not provider:
                return {'message': 'Service provider does not exist'}, 404

            #Lock wallet
            wallet = ProviderWallet.objects.select_for_update().filter(
                provider_id=provider_id
            ).first()

            if not wallet:
                return {
                    'message': 'Wallet not found. Add wallet before requesting payout'
                }, 400

            if wallet.balance < amount:
                return {'message': 'Insufficient funds'}, 400

            #Debit wallet
            wallet.balance -= amount
            wallet.save(update_fields=["balance"])

            payout_id = str(uuid.uuid4())
            reference_id = str(uuid.uuid4())

            #Ledger entry (IMMUTABLE)
            ProviderLedger.objects.create(
                provider_id=provider_id,
                reference_id=reference_id,
                entry_type='DEBIT',
                source='PAYOUT_REQUEST',
                amount=amount,
                description=f'Payout request {payout_id}'
            )

            # Payout request
            PayoutRequest.objects.create(
                provider_id=provider_id,
                payout_id=payout_id,
                amount=amount,
                status='PENDING'
            )

        return {
            'message': 'Payout request filed successfully',
            'payout_id': payout_id,
            'amount': str(amount),
            'status': 'PENDING'
        }, 200

    except Exception as e:
        print(f"Payout error: {e}")
        return {'message': 'Something went wrong'}, 500
