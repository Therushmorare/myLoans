# utils/qr.py
import qrcode
import io
import base64
import json

def generate_qr_base64(data: dict) -> str:
    """
    Generates a QR code from a dict and returns it as a base64 string.
    """
    payload = json.dumps(data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return base64.b64encode(buffer.read()).decode()