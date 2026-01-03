from background_task import background
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@background(schedule=0)
def send_mfa_email(email, user_type, code):
    subject = f"{user_type.capitalize()} MFA Verification Code"

    html_body = render_to_string(
        "email_templates/mfa.html",
        {
            "keyToken": code,
            "user_name": email
        }
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body="Your MFA code",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()
