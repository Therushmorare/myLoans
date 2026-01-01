from django.db import transaction
from decimal import Decimal
from django.utils import timezone
from loans_project.models.admin import AdminUser
from loans_project.models.service_provider import ServiceProvider
from loans_project.models.provider_wallet import ProviderWallet
from loans_project.models.provider_ledger import ProviderLedger
from loans_project.models.payout import PayoutRequest


def process_payout(payout_id, admin_id, status, comments=None):
    try:
        if status not in ["APPROVED", "REJECTED"]:
            return {'message': 'Invalid status'}, 400

        with transaction.atomic():

            # Validate admin
            admin = AdminUser.objects.filter(id=admin_id).first()
            if not admin:
                return {'message': 'Unauthorized'}, 403

            # Lock payout
            payout = PayoutRequest.objects.select_for_update().filter(
                id=payout_id
            ).first()

            if not payout:
                return {'message': 'Payout request not found'}, 404

            if payout.status != "PENDING":
                return {
                    'message': f'Payout already {payout.status.lower()}'
                }, 400

            payout.status = status
            payout.processed_at = timezone.now()
            payout.admin_id = str(admin_id)
            payout.comments = comments
            payout.save()

            # If rejected → refund provider wallet
            if status == "REJECTED":

                wallet = ProviderWallet.objects.select_for_update().filter(
                    provider_id=payout.provider_id
                ).first()

                if not wallet:
                    raise Exception("Provider wallet missing")

                wallet.balance += Decimal(payout.amount)
                wallet.save(update_fields=["balance"])

                ProviderLedger.objects.create(
                    provider_id=payout.provider_id,
                    reference_id=str(payout.id),
                    entry_type="CREDIT",
                    source="PAYOUT_REVERSAL",
                    amount=payout.amount,
                    description="Payout rejected, funds returned"
                )

            # If approved → money leaves platform
            if status == "APPROVED":
                ProviderLedger.objects.create(
                    provider_id=payout.provider_id,
                    reference_id=str(payout.id),
                    entry_type="DEBIT",
                    source="PAYOUT_APPROVED",
                    amount=payout.amount,
                    description="Payout approved for bank transfer"
                )

            return {
                'message': f'Payout {status.lower()} successfully',
                'payout_id': str(payout.id),
                'status': status
            }, 200

    except Exception as e:
        print(f"Payout Processing Error: {e}")
        return {'message': 'Something went wrong'}, 500