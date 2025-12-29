from decimal import Decimal
from django.db import transaction
import uuid
import logging
from loans_project.models.client_wallet import Wallet
from loans_project.models.client import Client

"""
Add client wallet
"""

logger = logging.getLogger(__name__)

def add_provider_wallet(user_id, bank, account_type, account_number):
    try:
        # Validate required fields
        if not all([user_id, bank, account_type, account_number]):
            return {'message': 'All fields are required'}, 400

        # Check provider existence
        client = Client.objects.filter(id=user_id).first()
        if not client:
            return {'message': 'User does not exist'}, 404

        # Prevent duplicate wallet for same account
        if Wallet.objects.filter(
            user_id=user_id,
            account_number=account_number
        ).exists():
            return {'message': 'Wallet already exists for this account'}, 409

        # Atomic transaction
        with transaction.atomic():
            Wallet.objects.create(
                id=uuid.uuid4(),
                user_id=user_id,
                bank=bank.strip(),
                account_type=account_type.strip(),
                account_number=account_number.strip(),
                balance=Decimal("0.00"),
                status="ACTIVE"
            )

        return {'message': 'Account added successfully'}, 201

    except Exception as e:
        logger.exception("Client wallet creation failed")
        return {'message': 'Something went wrong'}, 500
