import datetime
import requests
from django.conf import settings
from loans_project.models.client import Client
from loans_project.models.verifications import Verifications


# ---------------------------
# Luhn checksum
# ---------------------------
def luhn_checksum(id_number):
    total = 0
    digits = list(map(int, str(id_number)))[::-1]

    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d

    return total % 10 == 0


# ---------------------------
# Local SA ID validation
# ---------------------------
def validate_sa_id(id_number):
    if len(id_number) != 13 or not id_number.isdigit():
        return False, "ID must be 13 digits"

    try:
        datetime.datetime.strptime(id_number[:6], "%y%m%d")
    except ValueError:
        return False, "Invalid birth date"

    if not luhn_checksum(id_number):
        return False, "Invalid check digit"

    return True, "Valid SA ID"


# ---------------------------
# VerifyID API validation
# ---------------------------
def validate_id_via_api(id_number):
    api_url = settings.VERIFYID_API_URL
    api_key = settings.VERIFYID_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "id": id_number,
        "consent": True
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        success = data.get("success") or data.get("status") == "found"
        return success, data

    except requests.RequestException as e:
        print(f"VerifyID API error: {e}")
        return False, {"error": str(e)}


# ---------------------------
# Final identity verification
# ---------------------------
def validate_identity(user_id, id_number):
    try:
        user = Client.objects.filter(id=user_id).first()
        if not user:
            return {'message': 'User does not exist, please signup'}, 404

        # 1️⃣ Try API verification first
        api_valid, api_response = validate_id_via_api(id_number)
        if api_valid:
            Verifications.objects.create(
                user_id=user_id,
                id_number=id_number,
                source="API",
                status="VERIFIED"
            )
            return {'message': 'Identity verified via Home Affairs'}, 200

        # 2️⃣ Fallback to local validation
        local_valid, reason = validate_sa_id(id_number)
        if local_valid:
            Verifications.objects.create(
                user_id=user_id,
                id_number=id_number,
                source="LOCAL",
                status="VERIFIED"
            )
            return {'message': 'Identity verified locally'}, 200

        return {'message': 'Identity not verified'}, 400

    except Exception as e:
        print(f"Identity verification error: {e}")
        return {'message': 'Something went wrong'}, 500
