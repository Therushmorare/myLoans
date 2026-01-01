from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from loans_project.models.admin import AdminUser
from loans_project.models.disputes import Dispute, DisputeResponse
from loans_project.models.client_wallet import Wallet
from loans_project.models.wallet_ledger import WalletLedger


def respond_to_dispute(dispute_id, responder_id, responder_type, message):
    try:
        dispute = Dispute.objects.filter(
            dispute_id=dispute_id
        ).first()

        if not dispute:
            return {'message': 'Dispute does not exist'}, 404

        if dispute.status not in ["OPEN", "RESPONDED"]:
            return {'message': 'Dispute already resolved'}, 400

        DisputeResponse.objects.create(
            dispute_id=dispute_id,
            responder_id=responder_id,
            responder_type=responder_type,
            message=message
        )

        dispute.status = "RESPONDED"
        dispute.save(update_fields=["status"])

        return {
            'message': 'Response submitted successfully',
            'status': dispute.status
        }, 200

    except Exception as e:
        print(f"Dispute Response Error: {e}")
        return {'message': 'Something went wrong'}, 500