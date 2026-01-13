from loans_project.models.client import Client

"""
Update profile
"""

def edit_profile(id, username=None, email=None, phone_number=None):
    try:
        user = Client.objects.filter(id=id).first()
        if not user:
            return {'message': 'User does not exist'}, 404

        # prevent duplicate emails
        if email and Client.objects.filter(email=email).exclude(id=id).exists():
            return {'message': 'Email already in use'}, 400

        if username:
            user.username = username

        if email:
            user.email = email

        if phone_number:
            user.phone_number = phone_number

        user.save()

        return {'message': 'User profile updated successfully'}, 200

    except Exception as e:
        print(f"profile update error: {e}")
        return {'message': 'Something went wrong'}, 500