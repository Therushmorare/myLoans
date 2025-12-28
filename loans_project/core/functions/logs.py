from decimal import Decimal
from loans_project.models.logs import UserLogs
from loans_project.models.client import Client
from loans_project.models.admin import AdminUser
import uuid

"""
Log User Activity
"""

def log_user_activity(user_id, user_type, action):
    try:
        #check user exists
        user = Client.objects.filter(id=user_id).exists() or \
                AdminUser.objects.filter(id=user_id).exists()
        
        if not user:
            return {'message': 'User error'}, 404
        
        UserLogs.objects.create(
            user=user_id,
            action=action,
            user_type=user_type
        )
        print(f"User action logged successfully")
        return None
    except Exception as e:
        print(f"Could not log user action:{e}")
        return None