from decimal import Decimal
from django.db import transaction
import uuid
import logging
from loans_project.models.provider_wallet import ProviderWallet
from loans_project.models.service_provider import ServiceProvider
from loans_project.core.functions.logs import log_user_activity

"""
Add service provider wallet
"""

logger = logging.getLogger(__name__)

def add_provider_wallet(provider_id, bank, account_type, account_number):
    try:
        # Validate required fields
        if not all([provider_id, bank, account_type, account_number]):
            return {'message': 'All fields are required'}, 400

        # Check provider existence
        provider = ServiceProvider.objects.filter(provider_id=provider_id).first()
        if not provider:
            return {'message': 'Service provider does not exist'}, 404

        # Prevent duplicate wallet for same account
        if ProviderWallet.objects.filter(
            provider_id=provider_id,
            account_number=account_number
        ).exists():
            return {'message': 'Wallet already exists for this account'}, 409

        # Atomic transaction
        with transaction.atomic():
            ProviderWallet.objects.create(
                id=uuid.uuid4(),
                provider_id=provider_id,
                bank=bank.strip(),
                account_type=account_type.strip(),
                account_number=account_number.strip(),
                balance=Decimal("0.00"),
                status="ACTIVE"
            )

        return {'message': 'Account added successfully'}, 201

    except Exception as e:
        logger.exception("Provider wallet creation failed")
        return {'message': 'Something went wrong'}, 500
