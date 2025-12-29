from loans_project.models.service_provider import ServiceProvider
import uuid
from loans_project.models.product_transaction import ProductTransaction

def create_transaction(provider_id, item_name, quantity, amount, description):
    try:

        #Check provider existence
        provider = ServiceProvider.objects.filter(provider_id=provider_id).first()
        if not provider:
            return {'message': 'Service provider does not exist'}, 404
        
        if any (x is None for x in [item_name, quantity, amount, description]):
            return {'message': 'Please fill out all inputs'}, 400
        

        transaction_id = str(uuid.uuid4())

        

