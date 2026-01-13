from loans_project.models.client import Client

#Verifications Checker

def check_verifications(user_id):
    try:
        user = Client.objects.filter(id=user_id).first()

        if not user:
            return {'message': 'User does not exist'}, 404

        if not user.is_verified:
            return {'message': 'Please verify your account'}, 403

        return {'message': 'Account verified'}, 200

    except Exception as e:
        print(f"Verification Checker Error: {e}")
        return {'message': 'Something went wrong'}, 500
