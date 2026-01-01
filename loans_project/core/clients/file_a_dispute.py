import uuid
from django.db import transaction
from django.utils import timezone
from loans_project.models.client import Client
from loans_project.models.disputes import Dispute

"""
File disputes
"""

def file_dispute(raised_by_id, raised_by_type, target_id, target_type, reference_id, reference_type, dispute_type, description):
    try:
        if raised_by_type not in ["USER", "PROVIDER"]:
            return {'message': 'Invalid dispute initiator'}, 400

        if any(x is None for x in [
            raised_by_id, target_id, reference_id,
            dispute_type, description
        ]):
            return {'message': 'Please fill out all fields'}, 400

        dispute = Dispute.objects.create(
            raised_by_id=raised_by_id,
            raised_by_type=raised_by_type,
            target_id=target_id,
            target_type=target_type,
            reference_id=reference_id,
            reference_type=reference_type,
            dispute_type=dispute_type,
            description=description
        )

        return {
            'message': 'Dispute filed successfully',
            'dispute_id': dispute.dispute_id,
            'status': dispute.status
        }, 200

    except Exception as e:
        print(f"Dispute Error: {e}")
        return {'message': 'Something went wrong'}, 500