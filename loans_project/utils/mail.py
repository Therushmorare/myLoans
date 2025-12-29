from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging


def send_mail(subject, template, context, recipients):
    """
    Email Utility
    """
    try:
        html_body = render_to_string(template, context)
        text_body = "Please view this email in HTML format."

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients
        )

        email.attach_alternative(html_body, "text/html")
        email.send()

        return True

    except Exception as e:
        logging.error(f"Mail send error: {e}")
        return False
